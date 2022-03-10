import requests

from flask import request as flask_request
from flask_restful import Resource

devices = {}

class Registering(Resource):

    def post(self):
        pass


class Monitoring():

    def get_device_status(self, device: str = None):

        # get status of all devices
        if device is None: 
            return devices
        elif device in devices:
            return devices[device]

    def test(self):
        response = requests.get('http://localhost:6969')
        return response

mon = Monitoring()
response = mon.test()

print(response.headers)
# print(response.content)

content = response.content
content = content.decode('utf-8')
print(content)

