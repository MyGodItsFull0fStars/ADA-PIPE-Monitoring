import json
import socket
from typing import List, Union

from network_constants import RegisterEnum
from hardware_monitoring import HardwareMonitoring
from utils import Singleton

import urllib.request

def trim_prometheus_message(message: Union[str, List[bytes]]) -> str:
    print(f'\n\n\n{type(message), message}\n\n\n')
    if type(message) == str:
        message_list: List[str] = message.split('\n')
    elif type(message) == list:
        message = [msg.decode('utf-8') for msg in message]
        message = '\n'.join(message)
        message_list: List[str] = message.split('\n')
    message_list = [msg for msg in message_list if '#' not in msg and len(msg) > 0]
    return '\n'.join(message_list)
class NetworkHandler():

    def __init__(self, config_file_path: str = 'config.json', secure_connection: bool = False) -> None:

        with open(config_file_path) as file:
            json_file = json.load(file)
            self.__init_master_node_config(json_file)
            self.__init_network_config(json_file)
            self.http_protocol: str = 'https' if secure_connection else 'http'

    def get_master_config_info(self) -> dict:
        return self.master_node

    def get_master_node_ip(self) -> str:
        return self.master_node_ip

    def get_master_node_port(self) -> int:
        return self.master_node_port

    def get_hostname(self) -> str:
        return self.hostname

    def get_ip_address(self) -> str:
        return self.ip_address

    def get_network_port(self) -> int:
        return self.network_port

    def get_master_node_url(self, suffix: str = None) -> str:
        if suffix is None or type(suffix) is not str:
            return f'{self.http_protocol}://{self.get_master_node_ip()}:{self.get_master_node_port()}/'
        return f'{self.http_protocol}://{self.get_master_node_ip()}:{self.get_master_node_port()}/{suffix}'

    def get_device_url(self, suffix: str = None) -> str:
        if suffix is None or type(suffix) is not str:
            return f'{self.http_protocol}://{self.get_ip_address()}:{self.get_network_port()}/'
        return f'{self.http_protocol}://{self.get_ip_address()}:{self.get_network_port()}/{suffix}'

    def get_registering_payload(self, device_name: str = None) -> dict:
        registering_payload: dict = {
            RegisterEnum.DEVICE_NAME.value:  device_name if device_name is not None else self.get_hostname(),
            RegisterEnum.IP_ADDRESS.value: self.get_ip_address(),
            RegisterEnum.PORT_NUMBER.value: self.get_network_port(),
            RegisterEnum.HARDWARE_DESCRIPTION.value: {
                'cpu cores': {
                    'total': HardwareMonitoring.get_num_total_cpu_cores(),
                    'physical': HardwareMonitoring.get_num_physical_cpu_cores()
                },
                'cpu frequency': HardwareMonitoring.get_cpu_frequency().current,
                'total memory': HardwareMonitoring.get_virtual_memory(as_dict=False).total,
                'total storage': '',
            },
            RegisterEnum.PROMETHEUS.value: {
                'namespace': 'monitoring'
            },
        }
        return registering_payload

    def __init_master_node_config(self, json_file) -> None:
        self.master_node: dict = json_file['master_node']
        self.master_node_ip: str = self.master_node['IP']
        self.master_node_port: int = self.master_node['port']

    def __init_network_config(self, json_file) -> None:
        network_config: dict = json_file['network']
        self.network_port: int = network_config['port']
        self.hostname: str = socket.gethostname()
        try:
            self.ip_address = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
        except Exception:
            self.ip_address: str = socket.gethostbyname(self.hostname)




if __name__ == '__main__':
    ch = NetworkHandler()
    print(ch.get_ip_address())
