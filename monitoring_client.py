import prometheus_client
from flask import Flask, Response
from flask_cors import CORS
from prometheus_client import ProcessCollector, make_wsgi_app
from waitress import serve
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from data_collector import (DataCollectorResponses, StatusUpdateProvider,
                            request_metrics_wrap)
from registering_handler import RegisteringHandler

DEBUG_MODE: bool = True
HOST_NUMBER: str = '0.0.0.0'
PORT_NUMBER: int = 5500

app = Flask(__name__)
cors = CORS(app, resources={f'/*': {'origins': '*'}})


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
    return DataCollectorResponses.get_total_number_of_requests()


@app.route('/test')
def test():
    response = prometheus_client.generate_latest(ProcessCollector())
    return Response(response, mimetype='text/plain')


if __name__ == '__main__':

    register_handler = RegisteringHandler()

    connected = register_handler.register_resource()

    status_update_provider = StatusUpdateProvider()
    status_update_provider.start_background_thread()

    if DEBUG_MODE is True:
        # debug mode
        app.run(host=HOST_NUMBER, port=PORT_NUMBER, debug=True)

    else:
        # production mode
        # host_name = socket.gethostname()
        # IP_address = socket.gethostbyname(host_name)
        # print(f'Running on http://{IP_address}:{PORT_NUMBER}/ (Press CTRL+C to quit)')
        serve(app, port=PORT_NUMBER)
