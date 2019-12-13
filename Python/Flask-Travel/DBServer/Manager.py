from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from Tools.DataTools import *


db = SQLAlchemy()

def initDB(app):
    # 数据库配置和地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sharui12@127.0.0.1:3306/travel_product'
    # 关闭自动跟踪修改
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    currentDB = SQLAlchemy(app)
    global db
    db = currentDB
    print(db)
    print(currentDB)
    return db

manager = Blueprint('manager', __name__)
@manager.route('/initdb', methods=['GET'])

def initdb():
    from DBServer.User import UserTools
    from DBServer.Flight import addFlights
    from DBServer.Relationship import add_relationship
    # from DBServer.Route import TripsTools
    from DBServer.TravelInformation import TripsTools

    # from DBServer.TravelInformation import *
    # print(db)
    # # 全部删除
    # db.drop_all()
    #
    # user_Tools = UserTools()
    #
    # #创建
    # user_Tools.add(user_id='0001', name='王0', sex='男', phone=12222222222)
    # user_Tools.add(user_id='0002', name='王1', sex='女', phone=13333333333)
    # user = user_Tools.find(user_id='0001')
    # print(user)
    # addFlights(flight_id='0001',
    #            flight_name='阿联酋航空EK309',
    #            flight_status='未出行',
    #            flight_type='团队出发',
    #            flight_luggage_rules='行李规则',
    #            departure_city='北京首都T2',
    #            departure_date='2019/04/03',
    #            departure_time='07:25',
    #            arrival_city='迪拜T3',
    #            arrival_date='2019/04/04',
    #            arrival_time='11:35',
    #            flight_time='7h30m')
    #
    # add_relationship(user_id='0001', flights='0001')
    #
    # routeTools = RouteTools()
    # routeTools.addRouteProduct(desc="Day01")
    # routeTools.addRouteProduct(desc="Day02")
    # routeTools.addRouteProduct(desc="Day03")
    # routeTools.addRouteProduct(desc="Day04")
    # routeTools.addRouteProduct(desc="Day05")
    # routeTools.addRouteProduct(desc="Day06")
    # routeTools.addRouteList(date='2019-08-22', time='11:00', desc='去大悦城', product_id=2)
    # routeTools.addRouteList(date='2019-08-22', time='12:00', desc='去大悦城', product_id=2)
    # routeTools.addRouteList(date='2019-08-22', time='13:00', desc='去大悦城', product_id=2)
    # routeTools.addRouteList(date='2019-08-23', time='11:00', desc='去大悦城', product_id=3)
    # routeTools.addRouteList(date='2019-08-23', time='12:00', desc='去大悦城', product_id=3)
    # routeTools.addRouteList(date='2019-08-23', time='13:00', desc='去大悦城', product_id=3)
    # routeTools.addRouteList(date='2019-08-24', time='11:00', desc='去大悦城', product_id=4)
    # routeTools.addRouteList(date='2019-08-24', time='12:00', desc='去大悦城', product_id=4)
    # routeTools.addRouteList(date='2019-08-24', time='13:00', desc='去大悦城', product_id=4)

    TripsTools().add(name='行程1', user_id='0001')
    #
    return 'q_json'




#############数据库操作







