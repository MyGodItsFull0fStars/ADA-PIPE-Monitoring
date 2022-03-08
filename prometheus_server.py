from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from data_collector import DataCollector, DataCollectorResponses

from utils import request_metrics_wrap

app = Flask(__name__)

data_collector: DataCollector = DataCollector()


app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app, {'/metrics': make_wsgi_app()})

@app.route('/')
@request_metrics_wrap
def root():
    return DataCollectorResponses.get_total_number_of_requests()


@app.route('/device_status')
@request_metrics_wrap
def metrics():
    return DataCollectorResponses.get_device_status_response()

@app.route('/hardware_status')
@request_metrics_wrap
def get_hardware():
    return 'Super Powerful Hardware'


if __name__ == '__main__':
    app.run(debug=True)
