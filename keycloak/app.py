import json
import logging

from flask import Flask, g
from flask_oidc import OpenIDConnect
import requests

#logging.basicConfig(level=logging.DEBUG)
'''with open('c:/Python/codes/Autointelli/Flask/four_api/keycloak/client_secrets.json') as f:
    client = json.loads(f.read())
    print(client)'''
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'c:/Python/codes/Autointelli/Flask/four_api/keycloak/client_secrets.json',
    'OIDC_OPENID_REALM': 'master',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_SCOPES': ['openid'],
    'OIDC_OPENID_REALM': 'master',
    'TESTING': True,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})
#

oidc = OpenIDConnect(app=app)

@app.route('/private')
@oidc.require_login
def hello_me():
    """Example for protected endpoint that extracts private information from the OpenID Connect id_token.
       Uses the accompanied access_token to access a backend service.
    """

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            print ('access_token=<%s>' % access_token)
            headers = {'Authorization': 'Bearer %s' % (access_token)}
            
        except:
            print ("Could not service")

    return access_token

@app.route('/api', methods=['POST'])
@oidc.accept_token(require_token=True)
def hello_api():
    print("working")
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})

#, scopes_required=['openid']
@app.route('/logout')
def logout():
    """Performs local logout by removing the session cookie."""

    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'


if __name__ == '__main__':
    app.run(debug=True)


#http://localhost:8080/auth/realms/master/protocol/openid-connect/auth?client_id=autointelli&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foidc_callback&scope=openid&access_type=offline&response_type=code&state=eyJjc3JmX3Rva2VuIjogIlNCOGRIX1FweHpqX2pyN1FhY2Y1WlVTbGZCS2FHaUFOIiwgImRlc3RpbmF0aW9uIjogImV5SmhiR2NpT2lKSVV6VXhNaUo5LkltaDBkSEE2THk4eE1qY3VNQzR3TGpFNk5UQXdNQzl3Y21sMllYUmxJZy5nX1RlQ3hKVnJzUTljUzFXNTMyNU1TY1AycGtBODFraTVPX2JobnVoVVQzSjIxY3pfLXA0ZmVpdE9QbUdpVmNibE5zWjZTTk9lcHBKUFltVWtHbGRBUSJ9&openid.realm=master
#http://localhost:8080/auth/realms/master/protocol/openid-connect/auth?client_id=autointelli&response_type=code&scope=openid&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F%2A&state=e0ZxeOSKDR91BB4o&nonce=1YnKf3HDZaxFHYgW


#http://localhost:8080/auth/realms/master/protocol/openid-connect/auth?client_id=autointelli&redirect_uri=https%3A%2F%2Foidcdebugger.com%2Fdebug&scope=openid&response_type=token%20code&response_mode=form_post&nonce=pu1dhjjhnh


'''POST {tokenEndpoint}
Content-Type: application/x-www-form-urlencoded

grant_type = authorization_code&
code = 2c2a0275-ce38-4434-9dab-7efca9303957.784affd6-d5ab-48df-a148-20572fbd7f84.65b69ba7-6d6e-4172-a4d8-eff8dda1e634&
client_id = autointelli&
client_secret = {clientSecret}&
redirect_uri = https % 3A % 2F % 2Foidcdebugger.com % 2Fdebug'''

#http://127.0.0.1:5000/oidc_callback

''''("""your email is %s and your user_id is %s!
               <ul>
                 <li><a href="/">Home</a></li>
                 <li><a href="//localhost:8080/auth/realms/master/account?referrer=autointelli&referrer_uri=http://localhost:5000/private&">Account</a></li>
                </ul>""" % (email, user_id))'''
