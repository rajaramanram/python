from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(["localhost:9200"])
app = Flask(__name__)


@app.route('/create_team',methods=["POST"])
def create_team():
    data = request.get_json()
    #print(data)
    if not data and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})
    mandatory_field_list = ["TEAM","ASSIGNMENT","STATUS"]
    for i in mandatory_field_list:
        if i not in data:
            return jsonify({'status': False, 'data': 'No Data Found'})
    res = es.index(index='team', body=data)
    print(res)
    return jsonify({'status': True, 'data': 'Data Sent'})

@app.route('/get_team',methods=["GET"])
def get_team():
    response_status = es.search(index="team")
    get = response_status['hits']['hits']
    array_field = []
    for i in range(len(get)):
        iterate_field = get[i]['_source']
        array_field.append(iterate_field)
    #print(array_field)
    return jsonify({'status': True, 'data':array_field})


@app.route('/assign_team', methods=["POST"])
def assign_to_team():
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
        #print("id", id)
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
    else:
        return jsonify({'status': False, 'data': 'No Data Found'})

@app.route('/update_alert_status', methods=["GET","POST"])
def update_alert_status():
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
            get_team_name = response_status['hits']['hits'][0]['_source']["TEAM"]
            print(get_team_name)
            search_team = {
                "query": {
                    "match": {
                        "TEAM": data["TEAM"]
                    }
                }
            }
            search_team_es =  es.search(index="team", body=search_team)
            print(search_team_es)
            team_id= search_team_es['hits']['hits'][0]['_id']
            print(team_id)
            inline_status_var = f"ctx._source.STATUS='{var_status}';"
            update_team_status = {
                "script": {
                    "source": inline_status_var,
                    "lang": "painless"
                }
            }
            update_team_index = es.update(index="team",id=team_id, body=update_team_status)
            print(update_team_index)
            return jsonify({'status': True, 'data': "data_sent"})
        else:
            return jsonify({'status': False, 'data': 'No Data Found'})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    

