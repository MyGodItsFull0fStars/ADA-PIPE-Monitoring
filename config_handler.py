import json


class ConfigHandler:

    def __init__(self, config_file_path: str = 'config.json') -> None:

        with open(config_file_path) as file:
            json_file = json.load(file)
            self.master_node: dict = json_file['master_node']
            self.master_node_ip: str = self.master_node['IP']

    def get_master_config_info(self) -> dict:
        return self.master_node

    def get_master_node_ip(self) -> str:
        return self.master_node_ip


if __name__ == '__main__':
    ch = ConfigHandler()
    # print(ch.master_node)
    print(ch.get_master_node_ip())
