import prometheus_client
import threading
from prometheus_client import Summary, Counter, Histogram, Gauge, Info, CollectorRegistry
from flask import Response
from psutil import virtual_memory

import time, datetime

from hardware_monitoring import HardwareMonitoring

from constants import *


_INF = float('inf')

_metric_data: dict = {}
_metric_data[TOTAL_REQUEST_COUNTER] = Counter(
    'request_operations_total', 'The total number of processed requests')
_metric_data[REQUEST_TIME_HIST] = Histogram(
    'request_duration', 'Histogram for the duration in seconds', buckets=(0.1, 0.2, 0.5, 0.6, 1, _INF))

# _graphs[VIRTUAL_MEMORY] = Sum

_metric_data[CPU_LOAD_1_MIN] = Gauge(
    CPU_LOAD_1_MIN, 'The CPU load of the last minute')
_metric_data[CPU_LOAD_5_MIN] = Gauge(
    CPU_LOAD_5_MIN, 'The CPU load of the last 5 minutes')
_metric_data[CPU_LOAD_15_MIN] = Gauge(
    CPU_LOAD_15_MIN, 'The CPU load of the last 15 minutes')

        

class DataCollector():

    @staticmethod
    def update_hardware_metrics():
        DataCollector.add_current_virtual_memory()
        DataCollector.add_current_cpu_load()

    @staticmethod
    def increment_total_request_counter():
        _metric_data[TOTAL_REQUEST_COUNTER].inc()

    @staticmethod
    def get_total_request_counter() -> int:
        return _metric_data[TOTAL_REQUEST_COUNTER]

    @staticmethod
    def add_response_time(response_time):
        _metric_data[REQUEST_TIME_HIST].observe(response_time)

    @staticmethod
    def add_current_virtual_memory():
        pass

    @staticmethod
    def add_current_cpu_load():
        current_cpu_load = HardwareMonitoring.get_cpu_load_average(as_dict=True)
        _metric_data[CPU_LOAD_1_MIN].set(current_cpu_load[CPU_LOAD_1_MIN])
        _metric_data[CPU_LOAD_5_MIN].set(current_cpu_load[CPU_LOAD_5_MIN])
        _metric_data[CPU_LOAD_15_MIN].set(current_cpu_load[CPU_LOAD_15_MIN])


class DataCollectorResponses():

    @staticmethod
    def get_device_status_response() -> Response:
        response = [prometheus_client.generate_latest(
            v) for v in _metric_data.values()]
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
        print(HardwareMonitoring.get_cpu_load_average(as_dict=True))