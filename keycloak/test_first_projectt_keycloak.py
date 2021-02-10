from flask import Flask,request,jsonify
from elasticsearch import Elasticsearch
from time import gmtime
import time
import json
#import datetime
from time import mktime
from datetime import datetime
from flask_oidc import OpenIDConnect


es = Elasticsearch(["172.16.1.103:9200"])

app=Flask(__name__)
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
@app.route('/receive', methods=['GET','POST'])
@oidc.accept_token(require_token=True)
def receive_data():
    if request.method == 'GET':
      get_body = {
          "size": 20
      }
      response_status = es.search(
          index="first_project", doc_type='_doc', body=get_body)
      get = response_status['hits']['hits']
      array_field = []
      for i in range(len(get)):
        iterate_field = get[i]['_source']
        array_field.append(iterate_field)
      print(array_field)
      return jsonify({'status': True, 'data': array_field})
    else:
      data= request.get_json()
      if not data and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})
      mandatory_field_list=["CINAME","SEVERITY","SOURCE","SOURCE_TIME"]
      for i in mandatory_field_list:
          if i not in data:
            return jsonify({'status': False, 'data': 'No Data Found'})
      
      #check for same alert
      check_already={
          "query": {
              "bool": {
                "must": [],
                "filter": [
                  {
                    "bool": { 
                      "should": [
                        {
                          "match_phrase": {
                            "CINAME": data["CINAME"]
                          }
                        }
                      ],
                    "minimum_should_match":1
                      }
                    },
                    {
                    "bool": { 
                      "should": [
                        {
                          "match_phrase": {
                            "SUMMARY": data["SUMMARY"]
                          }
                        }
                      ],
                    "minimum_should_match":1
                      }
                    },
                    {
                    "bool": { 
                      "should": [
                        {
                          "match_phrase": {
                          "IP": data["IP"]
                          }
                        }
                      ],
                    "minimum_should_match":1
                      }
                    },
                    {
                    "bool": { 
                      "should": [
                        {
                          "match_phrase": {
                          "STATUS":"open"
                          }
                        }
                      ],
                    "minimum_should_match":1
                      }
                    }
                  ]
              }
            }
          }

      # get a response from the cluster
      response_status = es.search(index="first_project", doc_type='_doc', body=check_already)
      if len(response_status['hits']['hits']) != 0:
        id = response_status['hits']['hits'][0]['_id']
        print("id", id)
        update_count_body={
            "script" : {
              "source": "ctx._source.COUNT += params.count",
              "lang": "painless",
              "params" : {
                "count" : 1
              }
            }
          }
        update_count = es.update(index="first_project",doc_type='_doc',id=id,body=update_count_body)
        print(update_count)
      else:
        gmt_time = time.gmtime()
        gmt_time_to_dt = datetime.fromtimestamp(mktime(gmt_time))
        conversion_gmt = datetime.strftime(gmt_time_to_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
        #GETTNG document count from es for incrementing ALERT_ID
        refresh=es.indices.refresh(index='first_project')
        get_count_es=es.cat.count(index='first_project', params={"format": "json"})
        update_count = int(get_count_es[0]['count']) + 1
        alert_id_string = "AL0000000"
        len_count = len(str(update_count))
        put_alert_id = alert_id_string[:-len_count]+str(update_count)
        #print(put_alert_id)
        data["ALERT_ID"] = put_alert_id
        data["COUNT"] = 1
        data["STATUS"] = "open"
        if data["ENVIRONMENT"] == '':
          data["ENVIRONMENT"] = "default"
        data["CREATED_TIME"] = conversion_gmt
        #print(data)
        res = es.index(index='first_project', doc_type='_doc', body=data)
        #print(res)
      return jsonify({'status': True, 'data': 'Data Sent'})
if __name__=="__main__":
    app.run(debug=True)
