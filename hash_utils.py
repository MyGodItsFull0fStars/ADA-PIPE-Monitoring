"""
Generate stable hashes for Python data objects.
Contains no business logic.

The hashes should be stable across interpreter implementations and versions.

Supports dataclass instances, datetimes, and JSON-serializable objects.

Empty dataclass fields are ignored, to allow adding new fields without
the hash changing. Empty means one of: None, '', (), [], or {}.

The dataclass type is ignored: two instances of different types
will have the same hash if they have the same attribute/value pairs.

Sources:
    * Code: https://github.com/lemon24/reader/blob/1efcd38c78f70dcc4e0d279e0fa2a0276749111e/src/reader/_hash_utils.py
    * Article: https://death.andgravity.com/stable-hashing

"""
import dataclasses
import datetime
import hashlib
import json
from collections.abc import Collection
from typing import Any
from typing import Dict


# Implemented for https://github.com/lemon24/reader/issues/179


# The first byte of the hash contains its version,
# to allow upgrading the implementation without changing existing hashes.
# (In practice, it's likely we'll just let the hash change and update
# the affected objects again; nevertheless, it's good to have the option.)
#
# A previous version recommended using a check_hash(data, hash) -> bool
# function instead of direct equality checking; it was removed because
# it did not allow objects to cache the hash.

_VERSION = 0
_EXCLUDE = '_hash_exclude_'


def get_hash(data: object, as_bytes: bool = False) -> Any:
    prefix = _VERSION.to_bytes(1, 'big')
    digest = hashlib.sha1(_json_dumps(data).encode('utf-8')).digest()
    digest = prefix + digest[:-1]
    return digest if as_bytes else digest.hex()


def _json_dumps(data: object) -> str:
    return json.dumps(
        data,
        default=_json_default,
        # force formatting-related options to known values
        ensure_ascii=False,
        sort_keys=True,
        indent=None,
        separators=(',', ':'),
    )


def _json_default(data: object) -> Any:
    try:
        return _dataclass_dict(data)
    except TypeError:
        pass
    if isinstance(data, datetime.datetime):
        return data.isoformat(timespec='microseconds')
    raise TypeError(f"Object of type {type(data).__name__} is not JSON serializable")


def _dataclass_dict(data: object) -> Dict[str, Any]:
    # we could have used dataclasses.asdict()
    # with a dict_factory that drops empty values,
    # but asdict() is recursive and we need to intercept and check
    # the _hash_exclude_ of nested dataclasses;
    # this way, json.dumps() does the recursion instead of asdict()

    # raises TypeError for non-dataclasses
    fields = dataclasses.fields(data)
    # ... but doesn't for dataclass *types*
    if isinstance(data, type):
        raise TypeError("got type, expected instance")

    exclude = getattr(data, _EXCLUDE, ())

    rv = {}
    for field in fields:
        if field.name in exclude:
            continue

        value = getattr(data, field.name)
        if value is None or not value and isinstance(value, Collection):
            continue

        rv[field.name] = value

    return rv
