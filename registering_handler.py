from urllib import response
from network_utils import NetworkHandler
import requests


class RegisteringHandler:

    def __init__(self) -> None:

        self._network_handler = NetworkHandler()
        self.ip_address: str = self._network_handler.get_ip_address()
        self.port_number: int = self._network_handler.get_network_port()


    def register(self):
        master_node_register_url: str = self._network_handler.get_master_node_url('register')
        payload = self._network_handler.get_registering_payload()

        response = requests.post(url=master_node_register_url, json=payload)
        print(response.status_code)
        
        

    def unregister(self):
        master_node_register_url: str = self._network_handler.get_master_node_url('register')
        payload = self._network_handler.get_registering_payload()

        response = requests.delete(url=master_node_register_url, json=payload)
        print(response.status_code, response.text)


if __name__ == '__main__':
    rh = RegisteringHandler()

    # rh.register()
    rh.unregister()