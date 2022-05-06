
import threading
import time
from typing import Dict

import requests

from device_utils import Device, device_handler


class StatusUpdateRetriever():

    @staticmethod
    def retrieve_update():
        """Retrieves the monitoring data of all registered devices.
        """

        while True:
            all_devices: Dict[int, Device] = device_handler.get_all_devices()

            if len(all_devices.values()) == 0:
                print(all_devices)
                print('No devices registered')

            for device in all_devices.values():
                StatusUpdateRetriever._send_monitor_request(device)

            time.sleep(5)
            # yield

        

    @staticmethod
    def _send_monitor_request(device: Device):
        """Sends the request to a single Device

        Args:
            device (Device): registered device that will be send a request to send it's monitoring data
        """
        try:
            request_url: str = f'{device.get_url()}/device_status'
            response = requests.get(request_url)
            print(response.text)

        except ConnectionError as err:
            print(err)
        

    @staticmethod
    def start_background_thread():
        thread = threading.Timer(1, StatusUpdateRetriever.retrieve_update)
        thread.setDaemon(True)
        thread.start()
