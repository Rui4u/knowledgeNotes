from builtins import *
from flask import Flask
from flask_cors import CORS

from flask import request

from DBServer.Manager import *
from Tools.DataTools import *
from DBServer.User import find
from DBServer.Flight import findFlights

app = Flask(__name__)
CORS(app)
app.register_blueprint(manager)
db = initDB(app)


if __name__ == '__main__':
    app.run()


@app.route('/')
def hello_world():
    return '123'


@app.route('/login')
def login():
    id = request.args.get("id") or ''
    phone = request.args.get("phone") or ''
    name = request.args.get("name") or ''
    print(id)
    print(phone)
    print(name)

    json = backjson(serialize(find(id=id, phone=phone, name=name)))
    return json


@app.route('/flight')
def flight():
    id = request.args.get("id") or 0
    if isinstance(id, str):
        id = int(id)
    print(id)
    json = backjson(findFlights(id))
    return json




