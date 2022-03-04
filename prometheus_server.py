from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
import random

app = Flask(__name__)

_INF = float('inf')

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

@app.route('/')
def root():
    start = time.time()
    graphs['c'].inc()

    time.sleep(0.5 * random.random())
    end = time.time()
    graphs['h'].observe(end - start)
    return f'Time to compute: {end - start}'

@app.route('/metrics')
def metrics():
    response = [prometheus_client.generate_latest(v) for v in graphs.values()]
    return Response(response, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)