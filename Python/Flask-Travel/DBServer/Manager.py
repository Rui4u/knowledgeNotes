from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from Tools.DataTools import *

manager = Blueprint('manager', __name__)

db = SQLAlchemy()

def initDB(app):
    # 数据库配置和地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sharui12@127.0.0.1:3306/travel_user'
    # 关闭自动跟踪修改
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    currentDB = SQLAlchemy(app)
    global db
    db = currentDB
    print(db)
    print(currentDB)
    return db




@manager.route('/initdb', methods=['GET'])
def initdb():
    from DBServer.User import add, find
    from DBServer.Flight import addFlights
    print(db)
    # 全部删除
    db.drop_all()
    # 创建
    add(name='王0', sex='男', phone=12222222222)
    add(name='王1', sex='女', phone=13333333333)
    user = find(id=1)
    print(user)
    addFlights(flight_name='阿联酋航空EK309',
               flight_status='未出行',
               flight_type='团队出发',
               flight_luggage_rules='行李规则',
               departure_city='北京首都T2',
               departure_date='2019/04/03',
               departure_time='07:25',
               arrival_city='迪拜T3',
               arrival_date='2019/04/04',
               arrival_time='11:35',
               flight_time='7h30m',
               user_id=user.id)
    flight = user.flight[0]
    q_dict = serialize(flight)
    q_json = jsonify(q_dict)
    str1 = 'q_dict = %s \n q_json = %s' % (q_dict, q_json)
    print(str1)
    print('--')

    return q_json




#############数据库操作







