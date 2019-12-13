from builtins import *
from flask import Flask
from flask_cors import CORS

from flask import request

from DBServer.Manager import initDB, manager
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


@app.route('/travellist')
def travellist():
    from DBServer.TravelInformation import TripsTools
    from DBServer.Route import find_route_list,find_route_product
    id = request.args.get("id") or 0
    if isinstance(id, str):
        id = int(id)
    print(id)

    print(TripsTools().find('0001').first().travel_product_id)
    # 通过用户找到行程
    for trip in TripsTools().find('0001'):
        #        通过行程找到所包含的产品（每天行程为不同产品）
        for product in find_route_product(trip.travel_product_id):
            #        通过产品找到所包含的行程
            for result in find_route_list(product.id):
                print(result)
            print('\n')
        print('\n')

    # json = backjson(findFlights(id))
    return '123'


