import requests

from network_utils import NetworkHandler


class RegisteringHandler:

    def __init__(self) -> None:

        self._network_handler = NetworkHandler()
        self.ip_address: str = self._network_handler.get_ip_address()
        self.port_number: int = self._network_handler.get_network_port()
        self.master_node_register_url: str = self._network_handler.get_master_node_url(
            'register')

    def register_resource(self) -> bool:
        try:
            payload = self._network_handler.get_registering_payload()
            response = requests.post(
                url=self.master_node_register_url, json=payload)
            print(response.status_code, response.text)
            return True
        except Exception as err:
            print(err)
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
