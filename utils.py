from functools import wraps
from time import perf_counter

from data_collector import DataCollector


def request_metrics_wrap(func):
    @wraps(func)
    def wrap(*args, **kw):
        start_time = perf_counter()
        result = func(*args, **kw)
        DataCollector.increment_total_request_counter()
        end_time = perf_counter()
        DataCollector.add_response_time(end_time - start_time)
        return result
    return wrap
