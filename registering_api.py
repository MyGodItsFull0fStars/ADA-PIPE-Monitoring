from flask_restful import Resource
from flask import jsonify, request, abort, Response

from device_utils import Device, device_handler
from ADA_PIPE_Monitoring_Base.network_constants import RegisterEnum

from ADA_PIPE_Monitoring_Base.http_status_codes_and_exceptions import HttpResponse

class RegisteringREST(Resource):
    """REST API Service that is used to register devices for the monitoring service
    """

    def get(self):
        """Not sure if required
        """
        response = HttpResponse(200, device_handler.get_devices_as_json())
        return response.get_response()

    def post(self):
        """A device that will be monitored, will register itself via a POST method to the Master Node
        """
        if not request.json:
            print('Bad request!')
            abort(400, 'No JSON body found')

        received_json = request.json

        try:
            Device._is_valid(json_file=received_json, debug=True)
            device = Device(
                received_json[RegisterEnum.DEVICE_NAME.value],
                received_json[RegisterEnum.IP_ADDRESS.value],
                received_json[RegisterEnum.PORT_NUMBER.value],
                received_json[RegisterEnum.HARDWARE_DESCRIPTION.value],
                received_json[RegisterEnum.PROMETHEUS.value]
            )
            device_id = device.get_id()
            if device_handler.is_in_devices(device_id):
                return Response('Device already registered, for updating use REST PUT method', 409)

            success: bool = device_handler.add_device(device)

            if success:
                return Response('Created', 201)
            else:
                return Response('Bad Request', 400)

        except Exception as e:
            print('Could not register the device', e)

            abort(400)

    def put(self):
        if not request.json:
            print('Bad request!')
            abort(401)

        received_json = request.json

        try:
            device = Device(received_json)
            device_id = device.get_device_id()


            if device_handler.is_in_devices(device_id):
                return Response('Device not found', 409)

            device_handler.add_device(device)
            
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
            device = Device(received_json)
            device_id = device.get_device_id()

            device_handler.delete_device(device_id)
            return Response('Success', 200)

        except Exception:
            print('Could not unregister the device')
            return Response('Could not unregister the device', 409)
