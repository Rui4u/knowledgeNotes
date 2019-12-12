from DBServer.Manager import db
from Tools.DataTools import *


class Relationship(db.Model):
    __tablename__ = 'user_relationship'
    user_id = db.Column(db.String(16), primary_key=True)
    flights = db.Column(db.String(16))

    def __repr__(self):
        return 'user_id:%s  Flisghts: %s' % self.user_id,  self.flights


def find(user_id='', flights=''):

    if len(user_id) > 0:
        try:
            user = Relationship.query.filter_by(user_id=user_id).first()
            print(user.user_id)
            return user

        except Exception as e:
            print(e)
            db.session.rollback()
            return api_request_type.user_cant_find_by_id
    else:
        return api_request_type.failure_no_pars


def add_relationship(user_id='', flights=''):
    if len(user_id) > 0:
        try:
            db.create_all()
            relationship = Relationship(user_id=user_id, flights=flights)
            db.session.add(relationship)
            db.session.commit()
        except Exception as e:
            print(e)
            print('增加出错')
            db.session.rollback()
    else:
        print('user_id 和 name 为空')

def delete(user_id):

    try:
        user = Relationship.query.filter_by(user_id=user_id).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        print('删除出错')
        db.session.rollback()


def change():
    try:
        user = Relationship.query.filter_by(name='10').filter_by(sex='男').first()
        user.name = '改了'
        db.session.commit()
    except Exception as e:
        print(e)
        print('更改出错')
        db.session.rollback()


def deleteall():
    try:
        user = Relationship.query.delete()
        db.session.commit()
    except Exception as e:
        print(e)
        print('删除出错')
        db.session.rollback()
