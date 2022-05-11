from typing import Any, Dict

from flask import Response, Flask
from waitress import serve
from flask_cors import CORS
from flask_restful import Api

from device_utils import device_handler
from registering_api import RegisteringREST
from status_retriever import StatusUpdateRetriever


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


api.add_resource(RegisteringREST, '/register')


class MessageHelper():

    @staticmethod
    def decode_response_content(response: Response) -> str:
        content = response.content
        content = content.decode('utf-8')
        return content

    @staticmethod
    def convert_response_to_dict(response: Response) -> Dict[str, Any]:
        content = MessageHelper.decode_response_content(response)
        content_array = content.split('\n')
        content_array = [
            element for element in content_array if '#' not in element and len(element) > 0]

        content_dict: Dict[str, Any] = {}
        for elem in content_array:
            key, value = elem.split(' ')
            content_dict[key] = value
        return content_dict


class Monitoring():

    def get_device_status(self, device: str = None):

        # get status of all monitored_devices
        if device is None:
            return device_handler.get_all_devices()
        return device_handler.get_device(device)

    # def test(self):
    #     response = requests.get('http://127.0.0.1:5000/device_status')
    #     # response = requests.get('http://194.182.174.128:5000/device_status')
    #     return response


if __name__ == '__main__':
    StatusUpdateRetriever.start_background_thread()
    app.run(port=9100, debug=True)
