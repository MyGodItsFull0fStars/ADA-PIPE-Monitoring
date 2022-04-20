from typing import Dict
from dataclasses import dataclass

from network_constants import *
import hash_utils

@dataclass
class MonitoredDevice():

    device_name: str
    ip_address: str
    port_number: int
    hardware: dict = None
    _hash_exclude_: tuple = ('device_name', 'hardware')

    def get_id(self) -> str:
        """Returns the ID in form of a (stable) hash value

        Returns:
            str: a hash value that represents the ID of the MonitoredDevice
        """
        return hash_utils.get_hash(hash_utils._json_default(self))

    def _is_valid(self, json_file, debug: bool = False) -> bool:
        def error_msg(key_name):
            if debug:
                print(f'{key_name} key not found in json file')
        if not DEVICE_NAME_JSON_KEY in json_file:
            error_msg(DEVICE_NAME_JSON_KEY)
            return False
        if not IP_ADDRESS_JSON_KEY in json_file:
            error_msg(IP_ADDRESS_JSON_KEY)
            return False
        if not PORT_NUMBER_JSON_KEY in json_file:
            error_msg(PORT_NUMBER_JSON_KEY)
            return False

        return True


monitored_devices: Dict[int, MonitoredDevice] = {}


def get_devices_as_json() -> dict:
    return {key: hash_utils._json_default(value, exclude_fields=False) for key, value in monitored_devices.items()}
