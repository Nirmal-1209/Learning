from flask import Flask
from flask import make_response

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/no_content")
def no_content():
    return ({"message" : "No Content"}, 204)

@app.route("/exp")
def index_explicit():
    resp = make_response({"message":"Hello World!"})
    resp.status_code = 200
    return resp