from waitress import serve
from flask_rabbit_request_post import app


serve(app, host='0.0.0.0', port=8080)

