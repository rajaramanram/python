from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json
import requests
from flask_oidc import OpenIDConnect


es = Elasticsearch(["172.16.1.103:9200"])
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'c:/Python/codes/Autointelli/Flask/four_api/keycloak/client_secrets.json',
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


@app.route('/api', methods=['POST'])
@oidc.accept_token(require_token=True)
def hello_api():
    print("working")
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})

#, scopes_required=['openid']


@app.route('/logout')
@oidc.accept_token(require_token=True)
def logout():
    """Performs local logout by removing the session cookie."""

    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'

@app.route('/create_team',methods=["POST"])
@oidc.accept_token(require_token=True)
def create_team():
    try:
        data = request.get_json()
        #print(data)
        if not data and data != '':
            return jsonify({'status': False, 'data': 'No Data Found'})
        mandatory_field_list = ["TEAM","ASSIGNMENT"]
        for i in mandatory_field_list:
            if i not in data:
                return jsonify({'status': False, 'data': 'No Data Found'})
        res = es.index(index='team', body=data)
        print(res)
        return jsonify({'status': True, 'data': 'Data Sent'})
    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})

@app.route('/get_team',methods=["GET"])
@oidc.accept_token(require_token=True)
def get_team():
    try:
        response_status = es.search(index="team")
        get = response_status['hits']['hits']
        array_field = []
        for i in range(len(get)):
            iterate_field = get[i]['_source']
            array_field.append(iterate_field)
        #print(array_field)
        return jsonify({'status': True, 'data':array_field})
    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})


@app.route('/assign_team', methods=["POST"])
@oidc.accept_token(require_token=True)
def assign_to_team():
    try:
        data = request.get_json()
        search_alertid = {
            "query": {
                "match": {
                    "ALERT_ID": data["ALERT_ID"]
                }
            }
        }
        response_status= es.search(
            index="first_project", body=search_alertid)
        if len(response_status['hits']['hits']) != 0:
            id = response_status['hits']['hits'][0]['_id']
            print("id", id)
            get_dict = response_status['hits']['hits'][0]['_source']
            print (get_dict)
            if "TEAM" in get_dict:
                var_data = ","+data["TEAM"]
                print(var_data)
                inline_var = f"ctx._source.TEAM +='{var_data}';"
                #print(inline_var)
                assign_more_team = {
                    "script": {
                        "source":inline_var,
                        "lang": "painless"
                    }
                }
                assign_team = es.update(
                    index="first_project", id=id, body=assign_more_team)
                print(assign_team)
                return jsonify({'status': True, 'data': "data_sent"})

            else:
                var_data = data["TEAM"]
                inline_var= f"ctx._source.TEAM ='{var_data}'; ctx._source.STATUS='Assigned';"
                #print(inline_var)
                assign_team_body = {
                    "script": {
                        "source": inline_var,
                        "lang": "painless"
                        }
                    }
                assign_team = es.update(index="first_project", id=id, body=assign_team_body)
                print(assign_team)
                return jsonify({'status': True, 'data': "data_sent"})
            return jsonify({'status': False, 'data': 'No Data Found'})
    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})

@app.route('/update_alert_status', methods=["GET","POST"])
@oidc.accept_token(require_token=True)
def update_alert_status():
    try:
        if request.method == 'GET':
            response_status = es.search(index="team")
            get = response_status['hits']['hits']
            array_field = []
            for i in range(len(get)):
                iterate_field = get[i]['_source']
                array_field.append(iterate_field)
            return jsonify({'status': True, 'data': array_field})
        else:
            data = request.get_json()
            search_alertid = {
                "query": {
                    "match": {
                        "ALERT_ID": data["ALERT_ID"]
                    }
                }
            }
            response_status = es.search(
                index="first_project", body=search_alertid)
            print(response_status)
            
            if len(response_status['hits']['hits']) != 0:
                id = response_status['hits']['hits'][0]['_id']
                #var_data = data["TEAM"]
                var_status = data["STATUS"]
                inline_var = f"ctx._source.STATUS='{var_status}';"
                #print(inline_var)
                update_team_body = {
                    "script": {
                        "source": inline_var,
                        "lang": "painless"
                    }
                }
                update_status = es.update(index="first_project",id=id, body=update_team_body)
                print(update_status)
                return jsonify({'status': True, 'data': "data_sent"})
            else:
                return jsonify({'status': False, 'data': 'No Data Found'})
    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data':'Error '+ str(err)})
        

@app.route('/delete_alert', methods=["POST"])
@oidc.accept_token(require_token=True)
def delete_alert():
    try:
        data = request.get_json()
        search_alertid = {
            "query": {
                "match": {
                    "ALERT_ID": data["ALERT_ID"]
                }
            }
        }
        response_status = es.search(
            index="first_project", body=search_alertid)
        if len(response_status['hits']['hits']) != 0:
            id = response_status['hits']['hits'][0]['_id']
            print("id", id)
            delete_alert_var = es.delete(index="first_project",id=id)
            print(delete_alert_var)
            return jsonify({'status': True, 'data': "data_sent"})
        else:
            return jsonify({'status': False, 'data': 'No Data Found'})
    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})


@app.route('/get_count', methods=["GET"])
@oidc.accept_token(require_token=True)
def get_count():
    try:
        get_count_var = es.count(index="first_project")["count"]
        print(get_count_var)
        return jsonify({'status': True, 'data': get_count_var})

    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})

@app.route('/add_note', methods=["POST"])
@oidc.accept_token(require_token=True)
def add_note_to_alert():
    try:
        data = request.get_json()
        search_alertid = {
            "query": {
                "match": {
                    "ALERT_ID": data["ALERT_ID"]
                }
            }
        }
        response_status = es.search(
            index="first_project", body=search_alertid)
        if len(response_status['hits']['hits']) != 0:
            id = response_status['hits']['hits'][0]['_id']
            print("id", id)
            var_data = data["DESCRIPTION"]
            inline_var = f"ctx._source.DESCRIPTION ='{var_data}'; ctx._source.STATUS='Assigned';"
            #print(inline_var)
            add_note_body = {
                "script": {
                    "source": inline_var,
                    "lang": "painless"
                }
            }
            add_note_var = es.update(
                index="first_project", id=id, body=add_note_body)
            print(add_note_var)
            return jsonify({'status': True, 'data': 'Data Sent'})
        else:
            return jsonify({'status': False, 'data': 'No Data Found'})

    except Exception as err:
        print(str(err))
        return jsonify({'status': False, 'data': 'Error ' + str(err)})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    

