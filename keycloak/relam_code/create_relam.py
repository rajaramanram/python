from flask import Flask,request,Response,jsonify
import requests

app = Flask(__name__)

@app.route("/get_user_token",methods = ["POST"])
def get_user_token():
    body = request.get_json()
    url = "http://localhost:8080/auth/realms/master/protocol/openid-connect/token"
    response = requests.post(url, data=body)
    tokens_data = response.json()
    print(tokens_data)
    token = tokens_data["access_token"]
    return token

    #re=Response.json
    #print(re)
    

@app.route("/create_realm", methods=["POST"])
def create_realm():
    headers = request.headers
    #"enabled": true,
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    url = "http://localhost:8080/auth/admin/realms"
    body = request.get_json()
    response = requests.post(url, headers={'Authorization': token},data=body)
    tokens_data = response.json()
    print(tokens_data)
    #token = tokens_data["access_token"]
    return tokens_data


@app.route("/admin_reg", methods=["POST"])
def admin_reg():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    print(token)
    url = "http://localhost:8080/auth/admin/realms/autointelli/users"
    body = request.get_json()
    response = requests.post(url, headers={'Authorization': token}, data=body)
    tokens_data = response.json()
    print(tokens_data)
    #token = tokens_data["access_token"]
    return tokens_data


if __name__=="__main__":
    app.run(debug=True)
