
import json
import time
import os
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode



region = 'us-east-1'
userpool_id = os.environ["COGNITO_USER_POOL_ID"]
app_client_id = os.environ["COGNITO_CLI_ID"]
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']


def verify_token(token):
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        #print('Public key not found in jwks.json')
        return False, "PUBLIC_KEY_NOT_FOUND"
    public_key = jwk.construct(keys[key_index])
    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        #print('Signature verification failed')
        return False, "SIGNATURE_VERIFICATION_FAILED"
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        #print('Token is expired')
        return False, "EXPIRED"
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['client_id'] != app_client_id:
        #print('Token was not issued for this audience')
        return False, "INVALID_TOKEN"
    # now we can use the claims
    return True, claims
        