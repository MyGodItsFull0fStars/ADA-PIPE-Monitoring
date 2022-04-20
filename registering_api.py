from flask_restful import Resource
from flask import jsonify, request, abort

from device_utils import MonitoredDevice, monitored_devices, get_devices_as_json
from network_constants import (
    DEVICE_NAME_JSON_KEY,
    IP_ADDRESS_JSON_KEY,
    PORT_NUMBER_JSON_KEY
)


class RegisteringREST(Resource):
    """REST API Service that is used to register devices for the monitoring service
    """

    def get(self):
        """Not sure if required
        """
        response = jsonify(get_devices_as_json())
        response.status_code = 200
        return response

    def post(self):
        """A device that will be monitored, will register itself via a POST method to the Master Node
        """
        if not request.json:
            print('Bad request!')
            abort(401)

        received_json = request.json

        try:
            device = MonitoredDevice(
                received_json[DEVICE_NAME_JSON_KEY],
                received_json[IP_ADDRESS_JSON_KEY],
                received_json[PORT_NUMBER_JSON_KEY]
            )
            device_id = device.get_id()
            if device_id in monitored_devices.keys():
                return 'Device already registered, for updating use REST PUT method', 405

            monitored_devices[device_id] = device

            return 'Success', 201

        except Exception:
            print('Could not register the device')

            return 'NO!', 417

    def put(self):
        if not request.json:
            print('Bad request!')
            abort(401)

        received_json = request.json

        try:
            device = MonitoredDevice(received_json)
            device_id = device.get_device_id()

            monitored_devices[device_id] = device

            return 'Success', 201

        except Exception:
            print('Could not update the device')

            return 'NO!', 417

    def delete(self):
        if not request.json:
            print('Bad request!')
            abort(401)

        received_json = request.json

        try:
            device = MonitoredDevice(received_json)
            device_id = device.get_device_id()

            monitored_devices.pop(device_id)

            return 'Success', 201

        except Exception:
            print('Could not unregister the device')
            error_msg = 'NO!' if device.get_device_id(
            ) in monitored_devices else 'Device not registered'
            return error_msg, 417
