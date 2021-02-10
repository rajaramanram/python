from flask import Flask, jsonify,request
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata, ProviderMetadata
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.user_session import UserSession
import flask
from flask import session

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'Secret',
    'DEBUG': True,
    'OIDC_REDIRECT_URI': 'http://localhost:5000'
})
#'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
#'OIDC_TOKEN_TYPE_HINT': 'access_token'


@app.before_first_request
def initialize():
    print("session initialized")
    #flask.session["initialized"] = True
    get_session = flask.session
    print(get_session)


'''@app.before_request
def check():
    if not flask.session.get('initialized'):
        print("session not initialized")
        session['initialized'] = True


@app.before_request
def check2():
    if not flask.session.get('initialized'):
        print("session not initialized=2")
        session['initialized'] = True'''

provider_metadata = ProviderMetadata(issuer="http://localhost:8080/auth/realms/master", authorization_endpoint="http://localhost:8080/auth/realms/master/protocol/openid-connect/auth", jwks_uri="http://localhost:8080/auth/realms/master/protocol/openid-connect/certs")
#, userinfo_uri= "http://localhost:8080/auth/realms/master/protocol/openid-connect/userinfo",token_uri= "http://localhost:8080/auth/realms/master/protocol/openid-connect/token",token_introspection_uri= "http://localhost:8080/auth/realms/master/protocol/openid-connect/token/introspect"
#config = ProviderConfiguration(provider_metadata=provider_metadata, [client_configuration])
PROVIDER_NAME1 = 'default'
client_metadata = ClientMetadata(client_id='autointelli', client_secret='becaca34-3413-4120-857b-0c37ec1a4a74')
#client_metadata = ClientMetadata(client_id = 'security-admin-console', client_secret = '5991d968-8c6d-43fc-8960-57bbac1ba85c')

config = ProviderConfiguration(provider_metadata=provider_metadata, client_metadata=client_metadata)
#config = ProviderConfiguration(issuer="http://localhost:8080/auth/realms/master", client_metadata = client_metadata)
auth = OIDCAuthentication({PROVIDER_NAME1: config})

@app.route('/')
@auth.oidc_auth(PROVIDER_NAME1)
def login1():
    #print(auth.user_getfield('preferred_username'))
    #print(auth.valid_access_token)
    user_session = UserSession(flask.session)
    for i in flask.session:
        print(i)
    print("session")
    return jsonify(access_token=user_session.access_token, id_token=user_session.id_token, userinfo=user_session.userinfo)


@app.route('/logout')
@auth.oidc_logout
def logout():
    return "You've been successfully logged out!"
    

@auth.error_view
def error(error=None, error_description=None):
    return jsonify({'error': error, 'message': error_description})


if __name__ == '__main__':
    auth.init_app(app)
    app.run()
#http: // localhost: 8080/auth/realms/master/protocol/openid-connect/auth?client_id = security-admin-console & response_type = code & scope = openid & redirect_uri = http % 3A % 2F % 2Flocalhost % 3A8080 & state = oRkhr9udwWRKySmf & nonce = fUsmQICArk1lfHBZ
#http: // localhost: 8080/auth/realms/master/protocol/openid-connect/auth?client_id = security-admin-console & redirect_uri = http % 3A % 2F % 2Flocalhost % 3A8080 % 2Fauth % 2Fadmin % 2Fmaster % 2Fconsole % 2F % 23 % 2Frealms % 2Fmaster & state = 82f08d11-2808-4565-9e4e-aeea613723be & response_mode = fragment & response_type = code & scope = openid & nonce = e5e39cff-09d6-415d-9b6a-6684fb0eebd2 & code_challenge = pAnFfmwb6LOhqim0TA4pFY32zU3C-4wlI7kY4HaHc1U & code_challenge_method = S256
