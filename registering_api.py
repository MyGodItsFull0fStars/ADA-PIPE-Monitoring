from flask_restful import Resource
from flask import jsonify, request, abort, Response

from device_utils import MonitoredDevice, monitored_devices, get_devices_as_json
from network_constants import (
    DEVICE_NAME_JSON_KEY,
    IP_ADDRESS_JSON_KEY,
    PORT_NUMBER_JSON_KEY
)

from http_status_codes_and_exceptions import HttpResponse

class RegisteringREST(Resource):
    """REST API Service that is used to register devices for the monitoring service
    """

    def get(self):
        """Not sure if required
        """
        response = HttpResponse(200, get_devices_as_json())
        return response.get_response()

    def post(self):
        """A device that will be monitored, will register itself via a POST method to the Master Node
        """
        if not request.json:
            print('Bad request!')
            abort(400)

        received_json = request.json

        try:
            MonitoredDevice._is_valid(json_file=received_json, debug=True)
            device = MonitoredDevice(
                received_json[DEVICE_NAME_JSON_KEY],
                received_json[IP_ADDRESS_JSON_KEY],
                received_json[PORT_NUMBER_JSON_KEY]
            )
            device_id = device.get_id()
            if device_id in monitored_devices.keys():
                return Response('Device already registered, for updating use REST PUT method', 409)

            monitored_devices[device_id] = device

            return Response('Created', 201)

        except Exception as e:
            print('Could not register the device')

            abort(400)

    def put(self):
        if not request.json:
            print('Bad request!')
            abort(401)

        received_json = request.json

        try:
            device = MonitoredDevice(received_json)
            device_id = device.get_device_id()

            if device_id not in monitored_devices:
                return Response('Device not found', 409)

            monitored_devices[device_id] = device

            return Response('Updated', 200)

        except Exception:
            print('Could not update the device')
            return Response('Could not update the device', 409)

    def delete(self):
        if not request.json:
            print('Bad request!')
            abort(400)

        received_json = request.json

        try:
            device = MonitoredDevice(received_json)
            device_id = device.get_device_id()

            monitored_devices.pop(device_id)
            return Response('Success', 200)

        except Exception:
            print('Could not unregister the device')
            return Response('Could not unregister the device', 409)
