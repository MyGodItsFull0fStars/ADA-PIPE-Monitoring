from flask import Response, Flask

import prometheus_client
from prometheus_client import ProcessCollector
from flask import Flask
from waitress import serve
from flask_cors import CORS

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from data_collector import DataCollectorResponses, StatusUpdateHandler


from utils import request_metrics_wrap

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
    return 'Super Powerful Hardware'

@app.route('/test')
def test():
    response = prometheus_client.generate_latest(ProcessCollector())
    return Response(response, mimetype='text/plain')


if __name__ == '__main__':

    sh = StatusUpdateHandler()
    sh.start_background_thread()
    
    if DEBUG_MODE is True:
        # debug mode
        app.run(host=HOST_NUMBER, port=PORT_NUMBER, debug=True)

    else:
        # production mode
        # host_name = socket.gethostname()
        # IP_address = socket.gethostbyname(host_name)
        # print(f'Running on http://{IP_address}:{PORT_NUMBER}/ (Press CTRL+C to quit)')
        serve(app, port=PORT_NUMBER)


