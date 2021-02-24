from flask import Flask,request,jsonify,g, redirect, url_for
from flask_oidc import OpenIDConnect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SERVER_NAME'] = "localhost:5000"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS':'',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_SCOPES': ['openid'],
    'OIDC_OPENID_REALM': 'master',
    'TESTING': True,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})
#'OIDC_CLIENT_SECRETS': 'c:/Python/codes/Autointelli/Flask/four_api/keycloak/pg_tenant2/client_secrets.json',


class AlertModel(db.Model):
    __tablename__ = 'alert1'

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String())
    environment = db.Column(db.String())
    count = db.Column(db.Integer())

    def __init__(self, alert_id, environment, count):
        self.alert_id = alert_id
        self.environment = environment
        self.count = count


@app.route('/private', subdomain="<username>")
def web_change(username):
    #global oidc
    web_urls = {
            "web": {
                "issuer": "http://localhost:8080/auth/realms/"+username,
                "auth_uri": f"http://localhost:8080/auth/realms/{username}/protocol/openid-connect/auth",
                "client_id": "autointelli",
                "client_secret": "f60b5f85-b41c-4e0d-8c25-56a7d3a9acba",
                "redirect_uris": [
                    "http://127.0.0.1:5000/oidc_callback"
                ],
                "userinfo_uri": f"http://localhost:8080/auth/realms/{username}/protocol/openid-connect/userinfo", 
                "token_uri": f"http://localhost:8080/auth/realms/{username}/protocol/openid-connect/token",
                "token_introspection_uri": f"http://localhost:8080/auth/realms/{username}/protocol/openid-connect/token/introspect"
            }
        }
    
    #app.config[] = web_urls
    #'OIDC_CLIENT_SECRETS': web_urls,
    return redirect(url_for('oidc'))


oidc = OpenIDConnect(app=app)
@app.route('/oidc')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(
            oidc.credentials_store[user_id]).access_token
            print('access_token=<%s>' % access_token)

        except:
            print("Could not service")

    return access_token

@app.route('/receive', methods=['GET','POST'])
@oidc.accept_token(require_token=True)
def receive_data():
    if request.method == 'GET':
        #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rajaraman@localhost:5432/"+username
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rajaraman@localhost:5432/customer_b"
        alerts = AlertModel.query.all()
        results = [
            {
                "alert_id": alert.alert_id,
                "environment": alert.environment,
                "count": alert.count
            } for alert in alerts]

        return {"alerts": results}
if __name__=="__main__":
    app.run(debug=True)
