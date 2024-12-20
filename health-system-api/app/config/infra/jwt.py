import jwt, os
from flask import request, g
from functools import wraps
from flask import abort, make_response, jsonify
from app.config.infra.cognito_verifier import verify_token


class BusinessException(Exception):
    pass


def require_token(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if (not authorization or not authorization.startswith("Bearer ")):
            abort(make_response(jsonify(code=401, message="Required valid token", success=False), 401))
        else: 
            token = authorization.replace("Bearer ", "")
            status, claims = verify_token(token)

            if(status == False):
                abort(make_response(jsonify(code=401, message="Invalid token", success=False), 401))
            else:
                g.user_id = claims.get('sub')
                return api_method(*args, **kwargs)

    return check_api_key