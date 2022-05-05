
import threading
from typing import Dict

from device_utils import Device, device_handler


class StatusUpdateRetriever():

    @staticmethod
    def retrieve_update():
        """Retrieves the monitoring data of all registered devices.
        """
        all_devices: Dict[int, Device] = device_handler.get_all_devices()

    @staticmethod
    def _send_monitor_request(device: Device):
        """Sends the request to a single Device

        Args:
            device (Device): registered device that will be send a request to send it's monitoring data
        """
        pass

    @staticmethod
    def start_background_thread():
        thread = threading.Timer(0, StatusUpdateRetriever.retrieve_update)
        thread.setDaemon(True)
        thread.start()
