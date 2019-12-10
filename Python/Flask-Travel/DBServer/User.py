from DBServer.Manager import db
from Tools.DataTools import *


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    phone = db.Column(db.String(16))
    flight = db.relationship('Flights', backref='user')

    def __repr__(self):
        return 'User:%s ' % self.name

def find(name='', phone='', id=0):
    if isinstance(id, str):
        if id != '':
            id = int(id)
        else:
            id = 0

    if id > 0:
        try:
            user = User.query.filter_by(id=id).first()
            print(user.id)
            return user

        except Exception as e:
            print(e)
            db.session.rollback()
            return api_request_type.user_cant_find_by_id
    elif len(name) > 0 and len(phone) > 0:
        try:
            user = User.query.filter_by(phone=phone).filter_by(name=name).first()
            print(user.id)
            return user

        except Exception as e:
            print(e)

            db.session.rollback()
            return api_request_type.user_cant_find
    else:
        return api_request_type.failure_no_pars


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


def deleteall():
    try:
        user = User.query.delete()
        db.session.commit()
    except Exception as e:
        print(e)
        print('删除出错')
        db.session.rollback()
