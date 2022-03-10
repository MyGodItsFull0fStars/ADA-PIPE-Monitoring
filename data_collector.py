import prometheus_client
from prometheus_client import Summary, Counter, Histogram, Gauge, Info
from flask import Response
from psutil import virtual_memory

from hardware_monitoring import HardwareMonitoring

# NETWORK STATUS
TOTAL_REQUEST_COUNTER: str = 'total_request_counter'
REQUEST_TIME_HIST: str = 'response_time_histogram'
VIRTUAL_MEMORY: str = 'virtual_memory'

# HARDWARE STATUS AND INFO
HARDWARE_INFO: str = 'hardware_info'
HARDWARE_STATUS_CURRENT: str = 'hardware_status_current'
HARDWARE_STATUS_AVERAGE: str = 'hardware_status_average'


_INF = float('inf')

_graphs: dict = {}
_graphs[TOTAL_REQUEST_COUNTER] = Counter(
    'request_operations_total', 'The total number of processed requests')
_graphs[REQUEST_TIME_HIST] = Histogram(
    'request_duration', 'Histogram for the duration in seconds', buckets=(0.1, 0.2, 0.5, 0.6, 1, _INF))

# _graphs[VIRTUAL_MEMORY] = Sum



class DataCollector():

    @staticmethod
    def increment_total_request_counter():
        _graphs[TOTAL_REQUEST_COUNTER].inc()

    @staticmethod
    def get_total_request_counter() -> int:
        return _graphs[TOTAL_REQUEST_COUNTER]

    @staticmethod
    def add_response_time(response_time):
        _graphs[REQUEST_TIME_HIST].observe(response_time)

    @staticmethod
    def add_current_virtual_memory():
        pass

class DataCollectorResponses():

    @staticmethod
    def get_device_status_response() -> Response:
        response = [prometheus_client.generate_latest(
            v) for v in _graphs.values()]
        return Response(response, mimetype='text/plain')

    @staticmethod
    def get_total_number_of_requests() -> Response:
        response = prometheus_client.generate_latest(
            DataCollector.get_total_request_counter())
        return Response(response, mimetype='text/plain')
