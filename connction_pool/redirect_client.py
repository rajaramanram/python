from flask import Flask, request, jsonify, g,url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_oidc import OpenIDConnect


from urllib.parse import urlparse
import psycopg2
from psycopg2 import pool
app = Flask(__name__)
app.config['SERVER_NAME'] = "localhost:5000"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_SCOPES': ['openid'],
    'OIDC_OPENID_REALM': 'master',
    'TESTING': True,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})
#'OIDC_CLIENT_SECRETS': 'c:/Python/codes/Autointelli/Flask/four_api/postgre_multi_tenant/connction_pool/dummy_sample.json',
oidc = OpenIDConnect()


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
@app.before_first_request
def start():
    subdomain = urlparse(request.url).hostname.split('.')[0]
    print("subdomain==",subdomain)
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
    password="rajaraman", host="127.0.0.1", port="5432", database="customer_metadata")
    if(postgreSQL_pool):
        print("Connection pool created successfully")

    ps_connection = postgreSQL_pool.getconn()

    if(ps_connection):
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(
            f"select * from cusotmer_secret where sub_domain = '{subdomain}'")
        alert_records = ps_cursor.fetchall()
        print(alert_records)
        '''list_var = []
        re_uri = list_var.append(alert_records[0][6].format(
            "http", subdomain, "localhost", "5000"))
        print(re_uri)'''
        web_urls = {
            "web":{
                "issuer": alert_records[0][2].format("http", "localhost", "8080", subdomain),
                "auth_uri": alert_records[0][3].format("http", "localhost", "8080", subdomain),
                "client_id": alert_records[0][4].format("http", "localhost", "8080", subdomain),
                "client_secret": alert_records[0][5].format("http", "localhost", "8080", subdomain),
                "redirect_uris": [alert_records[0][6].format(
                    "http", "localhost", "5000")],
                "userinfo_uri": alert_records[0][7].format("http", "localhost", "8080", subdomain),
                "token_uri": alert_records[0][8].format("http", "localhost", "8080", subdomain),
                "token_introspection_uri": alert_records[0][9].format("http", "localhost", "8080", subdomain)
            }
        }
        print(web_urls)
        with open('c:/Python/codes/Autointelli/Flask/four_api/postgre_multi_tenant/connction_pool/client_secrets.json', 'w') as outfile:
            json_object = json.dumps(web_urls, indent=4)
            print(json_object)
            outfile.write(json_object)

    ps_cursor.close()
    #json_object = json.dumps(web_urls, indent=4)
    #print(json_object)
    #'OIDC_CLIENT_SECRETS': jsonify({'web':web_urls})
    #Flask/four_api/postgre_multi_tenant/connection_pool/
    #Autointelli/Flask/four_api/postgre_multi_tenant/
    app.config.update({'OIDC_CLIENT_SECRETS': 'c:/Python/codes/Autointelli/Flask/four_api/postgre_multi_tenant/connction_pool/client_secrets.json'})
    oidc.init_app(app)
    #oidc = OpenIDConnect(app=app)


@ app.route('/private', subdomain="<username>")
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    user_id = info.get('sub')
    print(user_id)
    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            print('access_token=<%s>' % access_token)

        except:
            print("Could not service")

    return access_token


@app.route('/receive', methods=['GET', 'POST'], subdomain="<username>")
@oidc.accept_token(require_token=True)
def receive_data():
    if request.method == 'GET':
        #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rajaraman@localhost:5432/"+username
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:rajaraman@localhost:5432/{username}"
        alerts = AlertModel.query.all()
        results = [
            {
                "alert_id": alert.alert_id,
                "environment": alert.environment,
                "count": alert.count
            } for alert in alerts]

        return {"alerts": results}


if __name__ == "__main__":
    #oidc.init_app(app)
    app.run(debug=True)
