from functools import wraps
from time import perf_counter
import enum

from data_collector import DataCollector


def request_metrics_wrap(func):
    @wraps(func)
    def wrap(*args, **kw):
        # start_time = perf_counter()
        result = func(*args, **kw)
        DataCollector.increment_total_request_counter()
        # end_time = perf_counter()
        # DataCollector.add_response_time(end_time - start_time)
        return result
    return wrap

class StrEnum(str, enum.Enum):
    """
    StrEnum is a Python `enum.Enum` that inherits from `str`.

    Example usage::

        class Example(StrEnum):
            UPPER_CASE = auto()
            lower_case = auto()
            MixedCase = auto()
    """

    def __new__(cls, value, *args, **kwargs):
        if not isinstance(value, (str, enum.auto)):
            raise TypeError(
                f"Values of StrEnums must be strings: {value!r} is a {type(value)}"
            )
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self):
        return str(self.value)

    def _generate_next_value_(name, *_):
        return name
