from DBServer.Manager import db
from Tools.DataTools import *


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
    flight_status = db.Column(db.String(16))
    # 团队出发  团队返回
    flight_type = db.Column(db.String(16))
    # 航班名称
    flight_name = db.Column(db.String(16))
    # 行李规定
    flight_luggage_rules = db.Column(db.String(16))

    flight_time = db.Column(db.String(16))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return 'User:%s ' % self.flight_name


def findFlights(id):
    if id > 0:
        try:
            flights = Flights.query.filter_by(user_id=id)
            flight_array = []

            for flight in flights:
                flight_array.append(flight)
            return flight_array

        except Exception as e:
            print(e)
            print('查找出错')
            db.session.rollback()
    else:
        return '参数出错'


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
               flight_time=None,
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
                             flight_time=flight_time,
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

