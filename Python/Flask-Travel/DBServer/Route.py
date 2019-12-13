from DBServer.Manager import *
from Tools.DataTools import *


class RouteList(db.Model):
    __tablename__ = 'tp_route_list'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    desc = db.Column(db.String(20))
    product_id = db.Column(db.Integer)

    def __repr__(self):
        return 'RouteList:date：%s, time:%s, desc:%s, product_id:%s' % (self.date, self.time, self.desc, self.product_id)


class RouteProduct(db.Model):
    __tablename__ = 'tp_route_product'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    desc = db.Column(db.String(500))
    trip_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return 'Route_list:%s ' % self.desc

class RouteTools:

    def addRouteList(self, date='', time='', desc='', product_id=0):
        try:
            trip = RouteList(date=date, time=time, desc=desc, product_id=product_id)
            db.session.add(trip)
            db.session.commit()
        except Exception as e:
            print(e)
            print('增加出错')
            db.session.rollback()

    def addRouteProduct(self, data='', desc='', trip_id=None):
        try:
            db.create_all()
            trip = RouteProduct(desc=desc, trip_id=trip_id)

            db.session.add(trip)
            db.session.commit()
        except Exception as e:
            print(e)
            print('增加出错')
            db.session.rollback()


def find_route_list(product_id=0):

    try:
        trips = RouteList.query.filter_by(product_id=product_id)
        return trips

    except Exception as e:
        print(e)
        db.session.rollback()
        return api_request_type.user_cant_find_by_id


def find_route_product(trip_id):

    try:
        trip_products = RouteProduct.query.filter_by(trip_id=trip_id)
        return trip_products

    except Exception as e:
        print(e)
        db.session.rollback()
        return api_request_type.user_cant_find_by_id