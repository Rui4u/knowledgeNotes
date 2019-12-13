from DBServer.Manager import *
from Tools.DataTools import *


class Trips(db.Model):
    __tablename__ = 'tp_Trips'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(300))
    user_id = db.Column(db.String(16))
    travel_product_id = db.Column(db.Integer)
    hotel_product_id = db.Column(db.Integer)

    def __repr__(self):
        return 'Trips:%s user_id:%s travel_product_id:%s hotel_product_id:%s' % (self.name, self.user_id,
                self.travel_product_id, self.hotel_product_id)


class TripsTools:

    def find(self, user_id=''):

        if len(user_id) > 0:
            try:
                trips = Trips.query.filter_by(user_id=user_id)
                return trips

            except Exception as e:
                print(e)
                db.session.rollback()
                return api_request_type.user_cant_find_by_id
        else:
            return api_request_type.failure_no_pars


    def add(self,
            name='',
            user_id='',
            travel_product_id=0,
            hotel_product_id=0
            ):

            try:
                db.create_all()
                trip = Trips(name=name, user_id=user_id, travel_product_id=travel_product_id, hotel_product_id=hotel_product_id)

                db.session.add(trip)
                db.session.commit()
            except Exception as e:
                print(e)
                print('增加出错')
                db.session.rollback()
