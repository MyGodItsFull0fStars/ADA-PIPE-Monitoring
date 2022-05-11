from typing import Dict, Union
from dataclasses import dataclass

from network_constants import RegisterEnum
import hash_utils

from utils import Singleton


@dataclass
class Device():

    device_name: str
    ip_address: str
    port_number: int
    hardware: dict = None
    prometheus: dict = None
    _hash_exclude_: tuple = ('device_name', 'hardware', 'prometheus')

    def get_id(self) -> str:
        """Returns the ID in form of a (stable) hash value

        Returns:
            str: a hash value that represents the ID of the MonitoredDevice
        """
        return hash_utils.get_hash(hash_utils._json_default(self))

    def get_url(self) -> str:
        return f'http://{self.ip_address}:{self.port_number}'

    @staticmethod
    def _is_valid(json_file, debug: bool = False) -> bool:
        def error_msg(key_name):
            if debug:
                print(f'{key_name} key not found in json file')
        if not RegisterEnum.DEVICE_NAME.value in json_file:
            error_msg(RegisterEnum.DEVICE_NAME)
            return False
        if not RegisterEnum.IP_ADDRESS.value in json_file:
            error_msg(RegisterEnum.IP_ADDRESS)
            return False
        if not RegisterEnum.PORT_NUMBER.value in json_file:
            error_msg(RegisterEnum.PORT_NUMBER)
            return False

        return True


class MonitorLogging():
    pass


class DeviceHandler(metaclass=Singleton):
    """This class will be used to store the registered devices
    """

    def __init__(self):
        self._monitored_devices: Dict[str, Device] = {}

    def get_all_devices(self) -> Dict[str, Device]:
        return self._monitored_devices

    def get_device(self, id: str) -> Device:
        if id is None or not type(str) or not type(int):
            return

        if type(int):
            return self._monitored_devices[str(id)]
        return self._monitored_devices[id]

    def add_device(self, device: Device) -> bool:
        if device._is_valid:
            self._monitored_devices[device.get_id()] = device
            return True
        else:
            print('Invalid Device encountered')
            return False

    def delete_device(self, device_id: str) -> bool:
        """Deletes a device from the registered devices

        Args:
            device_id (str): the id of the device

        Returns:
            bool: True if successfully removed, else returns False
        """
        return self.__delete_device(device_id)

    def __delete_device(self, device_id: Union[int, str]) -> bool:
        if device_id is None or len(device_id) == 0:
            return False

        if type(device_id) == int:
            device_id = str(device_id)

        if type(device_id) == float:
            device_id = str(round(device_id))

        if not self.is_in_devices(device_id):
            return False

        removed_device = self._monitored_devices.pop(device_id, None)
        # if None is returned, something went wrong
        return removed_device is not None

    def is_in_devices(self, id: int) -> bool:
        return id in self._monitored_devices

    def get_devices_as_json(self) -> dict:
        return {key: hash_utils._json_default(value, exclude_fields=True) for key, value in self._monitored_devices.items()}


device_handler: DeviceHandler = DeviceHandler()
