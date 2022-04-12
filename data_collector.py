from matplotlib.style import available
import prometheus_client
import threading
from prometheus_client import Summary, Counter, Histogram, Gauge, Info, CollectorRegistry
from flask import Response
from psutil import virtual_memory

import time, datetime

from hardware_monitoring import HardwareMonitoring

from metric_data import *       

class DataCollector():

    @staticmethod
    def update_hardware_metrics():
        DataCollector.update_current_virtual_memory()
        DataCollector.update_current_cpu_load()

    @staticmethod
    def increment_total_request_counter():
        metric_data[TOTAL_REQUEST_COUNTER].inc()

    @staticmethod
    def get_total_request_counter() -> int:
        return metric_data[TOTAL_REQUEST_COUNTER]

    @staticmethod
    def add_response_time(response_time):
        metric_data[REQUEST_TIME_HIST].observe(response_time)

    @staticmethod
    def update_current_virtual_memory():
        vm = HardwareMonitoring.get_virtual_memory()
        metric_data[VIRTUAL_MEMORY_AVAILABLE].set(vm['available'])
        metric_data[VIRTUAL_MEMORY_USED].set(vm['used'])
        metric_data[VIRTUAL_MEMORY_FREE].set(vm['free'])

    @staticmethod
    def update_current_cpu_load():
        current_cpu_load = HardwareMonitoring.get_cpu_load_average(as_dict=True)
        metric_data[CPU_LOAD_1_MIN].set(current_cpu_load[CPU_LOAD_1_MIN])
        metric_data[CPU_LOAD_5_MIN].set(current_cpu_load[CPU_LOAD_5_MIN])
        metric_data[CPU_LOAD_15_MIN].set(current_cpu_load[CPU_LOAD_15_MIN])


class DataCollectorResponses():

    @staticmethod
    def get_device_status_response() -> Response:
        response = [prometheus_client.generate_latest(
            v) for v in metric_data.values()]
        return Response(response, mimetype='text/plain')

    @staticmethod
    def get_total_number_of_requests() -> Response:
        response = prometheus_client.generate_latest(
            DataCollector.get_total_request_counter())
        return Response(response, mimetype='text/plain')

class StatusUpdateHandler():

    @staticmethod
    def update_status():
        while True:
            DataCollector.update_hardware_metrics()
            time.sleep(1)

    @staticmethod
    def start_background_thread():
        threading.Timer(0, StatusUpdateHandler.update_status).start()
        # print(HardwareMonitoring.get_cpu_load_average(as_dict=True))