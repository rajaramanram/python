from flask import Flask, request, jsonify, g
from flask_oidc import OpenIDConnect
from flask_sqlalchemy import SQLAlchemy
import json

import psycopg2
from psycopg2 import pool
postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
    password="rajaraman", host="127.0.0.1", port="5432", database="customer_metadata")
if(postgreSQL_pool):
    print("Connection pool created successfully")

ps_connection = postgreSQL_pool.getconn()

if(ps_connection):
    ps_cursor = ps_connection.cursor()
    ps_cursor.execute(
        "select * from cusotmer_secret where sub_domain = 'customer_c'")
    alert_records = ps_cursor.fetchall()
    #print(alert_records)
    web_urls = {
        "web": {
            "issuer": alert_records[0][2],
            "auth_uri": alert_records[0][3],
            "client_id": alert_records[0][4],
            "client_secret": alert_records[0][5],
            "redirect_uris": alert_records[0][6],
            "userinfo_uri": alert_records[0][7],
            "token_uri": alert_records[0][8],
            "token_introspection_uri": alert_records[0][9]
        }
    }
    print(web_urls)

ps_cursor.close()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': str(web_urls),
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


@app.route('/private')
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


@app.route('/receive', methods=['GET', 'POST'])
@oidc.accept_token(require_token=True)
def receive_data():
    if request.method == 'GET':
        #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rajaraman@localhost:5432/"+username
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rajaraman@localhost:5432/customer_c"
        alerts = AlertModel.query.all()
        results = [
            {
                "alert_id": alert.alert_id,
                "environment": alert.environment,
                "count": alert.count
            } for alert in alerts]

        return {"alerts": results}


if __name__ == "__main__":
    app.run(debug=True)
