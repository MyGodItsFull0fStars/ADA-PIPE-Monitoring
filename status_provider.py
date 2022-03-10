from flask import Response, Flask, request
from flask_restful import Api

import prometheus_client
from prometheus_client import ProcessCollector
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from data_collector import DataCollector, DataCollectorResponses

from utils import request_metrics_wrap

app = Flask(__name__)



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

@app.route('/test')
def test():
    response = prometheus_client.generate_latest(ProcessCollector())
    return Response(response, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
