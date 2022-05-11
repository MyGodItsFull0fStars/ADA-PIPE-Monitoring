import time
import requests

from network_utils import NetworkHandler


class RegisteringHandler:

    def __init__(self) -> None:

        self._network_handler = NetworkHandler()
        self.ip_address: str = self._network_handler.get_ip_address()
        self.port_number: int = self._network_handler.get_network_port()
        self.master_node_register_url: str = self._network_handler.get_master_node_url(
            'register')

    def register_resource(self, connection_attempts: int = 3, connection_delay: int = 5) -> bool:
        connected: bool = False

        for t in range(0, connection_attempts + 1):
            if not connected:
                time.sleep(t*connection_delay)
                print('test')
            else:
                break
            connected = self.__register_resource()
        if not connected:
            raise ConnectionError('Resource could not be registered')

    def __register_resource(self) -> bool:
        try:
            payload = self._network_handler.get_registering_payload()
            response = requests.post(
                url=self.master_node_register_url, json=payload)
            print(response.status_code, response.text)
            return True
        except Exception as err:
            return False

    def update(self):
        pass

    def unregister(self):

        payload = self._network_handler.get_registering_payload()

        response = requests.delete(
            url=self.master_node_register_url, json=payload)
        print(response.status_code, response.text)


if __name__ == '__main__':
    rh = RegisteringHandler()

    rh.register_resource()
    # rh.unregister()
