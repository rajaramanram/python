#from threading import *
from flask import Flask
from flask_restful import Resource,Api
import time
import threading
app = Flask(__name__)
api = Api(app)

def task():
    print("started______________________________________Task")
    print(threading.current_thread().name)
    time.sleep(10)
    print("com__________________________________________pleted")
class hello(Resource):
    def get(self):
        threading.Thread(target=task).start()
        return {'hello':'world'}
api.add_resource(hello,"/")
if __name__ =="__main__":
    app.run(debug=True)
