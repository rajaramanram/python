from flask import Flask
app=Flask(__name__)
@app.route('/')
def index():
    return "<h1>ai index/h1>"
@app.route('/contact')
def contact():
    return "<h1>rajaraman ai contact</h1>"
if __name__=="__main__":
    app.run(debug=True)