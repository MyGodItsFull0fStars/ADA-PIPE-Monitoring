from prometheus_client import Summary, Counter, Histogram, Gauge, Info, CollectorRegistry

_INF = float('inf')

metric_data: dict = {}

# NETWORK STATUS
TOTAL_REQUEST_COUNTER: str = 'total_request_counter'
REQUEST_TIME_HIST: str = 'response_time_histogram'

metric_data[TOTAL_REQUEST_COUNTER] = Counter(
    'request_operations_total', 'The total number of processed requests')


# HARDWARE STATUS AND INFO
HARDWARE_INFO: str = 'hardware_info'

CPU_LOAD_1_MIN: str = 'cpu_load_last_minute'
CPU_LOAD_5_MIN: str = 'cpu_load_5_minutes'
CPU_LOAD_15_MIN: str = 'cpu_load_15_minutes'

metric_data[CPU_LOAD_1_MIN] = Gauge(
    CPU_LOAD_1_MIN, 'The CPU load of the last minute')
metric_data[CPU_LOAD_5_MIN] = Gauge(
    CPU_LOAD_5_MIN, 'The CPU load of the last 5 minutes')
metric_data[CPU_LOAD_15_MIN] = Gauge(
    CPU_LOAD_15_MIN, 'The CPU load of the last 15 minutes')

HARDWARE_STATUS_AVERAGE: str = 'hardware_status_average'

# VIRTUAL MEMORY
VIRTUAL_MEMORY: str = 'virtual_memory'
VIRTUAL_MEMORY_AVAILABLE: str = VIRTUAL_MEMORY + '_available'
VIRTUAL_MEMORY_USED: str = VIRTUAL_MEMORY + '_used'
VIRTUAL_MEMORY_FREE: str = VIRTUAL_MEMORY + '_free'

metric_data[VIRTUAL_MEMORY_AVAILABLE] = Gauge(VIRTUAL_MEMORY_AVAILABLE, 'Available Virtual Memory')
metric_data[VIRTUAL_MEMORY_USED] = Gauge(VIRTUAL_MEMORY_USED, 'Used Virtual Memory')
metric_data[VIRTUAL_MEMORY_FREE] = Gauge(VIRTUAL_MEMORY_FREE, 'Free Virtual Memory')



# _graphs[VIRTUAL_MEMORY] = Sum


