from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello Christian</h1>'

@app.route('/test')
def netdata():
    bla = requests.get('http://localhost:19999/api/v1/allmetrics')
    return bla.content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)