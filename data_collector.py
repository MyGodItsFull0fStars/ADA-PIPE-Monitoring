import threading
import time

import prometheus_client
from flask import Response


from hardware_monitoring import HardwareMonitoring
from metric_data import *
from functools import wraps


def request_metrics_wrap(func):
    @wraps(func)
    def wrap(*args, **kw):
        # from time import perf_counter
        # start_time = perf_counter()
        result = func(*args, **kw)
        DataCollector.increment_total_request_counter()
        # end_time = perf_counter()
        # DataCollector.add_response_time(end_time - start_time)
        return result
    return wrap


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

    # @staticmethod
    # def add_response_time(response_time):
    #     metric_data[REQUEST_TIME_HIST].observe(response_time)

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

class StatusUpdateProvider():

    @staticmethod
    def update_status():
        while True:
            DataCollector.update_hardware_metrics()
            time.sleep(1)

    @staticmethod
    def start_background_thread():
        threading.Timer(0, StatusUpdateProvider.update_status).start()
        # print(HardwareMonitoring.get_cpu_load_average(as_dict=True))
