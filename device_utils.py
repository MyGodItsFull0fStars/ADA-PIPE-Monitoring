from typing import Dict
from flask import Response


class MonitoredDevice():

    def __init__(self, json_file) -> None:
        print(json_file)
        if self._is_valid(json_file):
            self.device_name: str = json_file['device_name']
            self.ip_address: str = json_file['ip_address']
            self.port_number: int = json_file['port_number']
        else:
            raise Exception

    def get_device_id(self) -> str:
        return hash(self.get_string_representation())

    def get_device_name(self) -> str:
        return self.device_name

    def get_ip_address(self) -> int:
        return self.ip_address

    def get_port_number(self) -> int:
        return self.port_number

    def _is_valid(self, json_file) -> bool:
        def error_msg(key_name):
            print(f'{key_name} key not found in json file')
        if not 'device_name' in json_file:
            error_msg('device_name')
            return False

        return True

    def get_string_representation(self) -> str:
        return '{' + f'device_name: {self.device_name}, ip_address: {self.ip_address}, port_number: {self.port_number}' + '}'

    def get_as_dict(self) -> dict:
        return {
            'device_name': self.device_name,
            'ip_address': self.ip_address,
            'port_number': self.port_number
            }

    def __str__(self) -> str:
        return f'device_name: {self.device_name}'


monitored_devices: Dict[int, MonitoredDevice] = {}


def get_devices_as_json() -> dict:
    return {key: value.get_as_dict() for key, value in monitored_devices.items()}
