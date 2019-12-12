from builtins import *
from flask import Flask
from flask_cors import CORS

from flask import request

from DBServer.Manager import *
from Tools.DataTools import *
from DBServer.User import UserTools
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
    user_id = request.args.get("id") or ''
    phone = request.args.get("phone") or ''
    name = request.args.get("name") or ''
    print(user_id)
    print(phone)
    print(name)
    user_tools = UserTools()
    user = user_tools.find(name, phone, user_id)
    print(user)
    json = backjson(serialize(user))
    return json


@app.route('/flight')
def flight():
    id = request.args.get("id") or 0
    if isinstance(id, str):
        id = int(id)
    print(id)
    json = backjson(findFlights(id))
    return json




