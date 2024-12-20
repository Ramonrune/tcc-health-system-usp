import jwt, os
from flask import request, g
from functools import wraps
from flask import abort, make_response, jsonify
from app.config.core.security.cognito_verifier import verify_token
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
                g.company_id = request.headers.get("Company-Id", None)
                g.sub = claims.get('sub')
                g.token = token
                g.decoded_jwt = claims
                return api_method(*args, **kwargs)

    return check_api_key