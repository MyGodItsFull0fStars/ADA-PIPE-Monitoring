import requests


devices = {}

class Monitoring():

    def get_device_status(self, device: str = None):

        # get status of all devices
        if device is None: 
            return devices
        elif device in devices:
            return devices[device]

    def test(self):
        response = requests.get('http://localhost:5000')
        return response

mon = Monitoring()
response = mon.test()

print(response.content)