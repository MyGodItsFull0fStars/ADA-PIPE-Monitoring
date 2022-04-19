import json
import socket

from network_constants import *

class NetworkHandler:

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
            DEVICE_NAME_JSON_KEY:  device_name if device_name is not None else self.get_hostname(),
            IP_ADDRESS_JSON_KEY: self.get_ip_address(),
            PORT_NUMBER_JSON_KEY: self.get_network_port(),
            PROMETHEUS_JSON_KEY: {
                'namespace': 'monitoring'
            }
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
        self.ip_address: str = socket.gethostbyname(self.hostname)


if __name__ == '__main__':
    ch = NetworkHandler()
    # print(ch.master_node)
    print(ch.get_hostname())
    print(ch.get_master_node_ip())
    print(ch.get_network_port())
    print(ch.get_master_node_url('register'))
