from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
CORS(app)
# 数据库配置和地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sharui12@127.0.0.1:3306/travel_user'
# 关闭自动跟踪修改
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    phone = db.Column(db.String(16))
    flight = db.relationship('Flights', backref='user')

    def __repr__(self):
        return 'User:%s ' % self.name


class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    departure_date = db.Column(db.String(16))
    arrival_date = db.Column(db.String(16))
    departure_time = db.Column(db.String(16))
    arrival_time = db.Column(db.String(16))
    departure_city = db.Column(db.String(16))
    arrival_city = db.Column(db.String(16))
    # 状态 1 已完成 0 待出发
    flight_status = db.Column(db.Integer)
    # 团队出发  团队返回
    flight_type = db.Column(db.String(16))
    # 航班名称
    flight_name = db.Column(db.String(16))
    # 行李规定
    flight_luggage_rules = db.Column(db.String(16))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return 'User:%s ' % self.flight_name


def addFlights(flight_name,
               flight_status=None,
               flight_type=None,
               flight_luggage_rules=None,
               departure_date=None,
               arrival_date=None,
               departure_time=None,
               arrival_time=None,
               departure_city=None,
               arrival_city=None,
               user_id=None
               ):
    if len(flight_name):
        try:
            db.create_all()
            flight = Flights(flight_name=flight_name,
                             flight_status=flight_status,
                             flight_type=flight_type,
                             flight_luggage_rules=flight_luggage_rules,
                             departure_city=departure_city,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             arrival_city=arrival_city,
                             arrival_date=arrival_date,
                             arrival_time=arrival_time,
                             user_id=user_id
                             )
            db.session.add(flight)

            db.session.commit()

        except Exception as e:
            print(e)
            print('增加航空信息出错')
            db.session.rollback()
    else:
        print('名字为空')

@app.route('/')
def hello_world():
    return '123'


if __name__ == '__main__':
    app.run()


@app.route('/adds', methods=['GET'])
def adds():

    db.drop_all()
    add(name='王0', sex='男', phone=12222222222)
    add(name='王1', sex='女', phone=13333333333)
    user = find(name='王0')
    addFlights(flight_name='阿联酋航空EK309',
               flight_status=0,
               flight_type='团队出发',
               flight_luggage_rules='行李规则',
               departure_city='北京首都T2',
               departure_date='2019/04/03',
               departure_time='07:25',
               arrival_city='迪拜T3',
               arrival_date='2019/04/04',
               arrival_time='11:35',
               user_id=user.id)
    user = find(name='王0')
    print('--')
    flight = user.flight[0]
    q_dict = serialize(flight)
    q_json = jsonify(q_dict)
    str1 = 'q_dict = %s \n q_json = %s' % (q_dict, q_json)
    print(str1)
    print('--')

    return q_json


def add(name, sex=None, phone=None):
    if len(name):
        try:
            db.create_all()
            user1 = User(name=name, sex=sex, phone=phone)
            db.session.add(user1)

            db.session.commit()

        except Exception as e:
            print(e)
            print('增加出错')
            db.session.rollback()
    else:
        print('名字为空')


def find(name=None):

    try:
        user = User.query.filter_by(name=name).first()
        print(user.id)
        return user

    except Exception as e:
        print(e)
        print('查找出错')
        db.session.rollback()


def findFlights(name=None):

    try:
        flight = Flights.query.filter_by().first()
        print(flight.id)
        print(flight.user_id)
        return flight

    except Exception as e:
        print(e)
        print('查找出错')
        db.session.rollback()

def delete(id):
    try:
        user = User.query.filter_by(id=28).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        print('删除出错')
        db.session.rollback()


def change():
    try:
        user = User.query.filter_by(name='10').filter_by(sex='男').first()
        user.name = '改了'
        db.session.commit()
    except Exception as e:
        print(e)
        print('更改出错')
        db.session.rollback()


def deleteAll():
    try:
        user = User.query.delete()
        db.session.commit()
    except Exception as e:
        print(e)
        print('删除出错')
        db.session.rollback()



def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)