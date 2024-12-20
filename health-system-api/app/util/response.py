from flask import  make_response, jsonify
from datetime import datetime

class Response:

    def ok(data, message = "Sucessfully"):
        return make_response(
            jsonify(
                code=200,
                success=True,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            200
        )

    def created(data, message = "Sucessfully"):
        return make_response(
            jsonify(
                code=201,
                success=True,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            201
        )

    def bad_request(message = "BadRequest", data=None):
        return make_response(
            jsonify(
                code=400,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            400
        )

    def unauthorized(message = "Unauthorized", data=None):
        return make_response(
            jsonify(
                code=401,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            401
        )
        
    def forbidden(message = "Forbidden", data = None):
        return make_response(
            jsonify(
                code=403,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            403
        )

    def not_found(message = "Not found", data=None):
        return make_response(
            jsonify(
                code=404,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            404
        )

    def conflict(message = "", data = None):
        return make_response(
            jsonify(
                code=409,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            409
        )


    def error(message = "Error", data = None):
        return make_response(
            jsonify(
                code=500,
                success=False,
                message=message,       
                data = data,
                timestamp=datetime.today()
            ),
            500
        )
