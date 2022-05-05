from dataclasses import dataclass
import mimetypes
from werkzeug.exceptions import HTTPException
from flask import jsonify, make_response
from dataclasses import dataclass

@dataclass
class HttpResponse():
    status_code: int
    response_json: dict
    mimetype: str = 'application/json'

    def get_response(self):
        return make_response(jsonify(self.response_json), self.status_code)

class InsufficientStorage(HTTPException):
    code = 507
    description = 'Not enough storage space.'