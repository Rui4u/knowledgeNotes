from DBServer.Manager import *
from Tools.DataTools import *

class User(db.Model):
    __tablename__ = 'tp_user'
    user_id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(16))
    sex = db.Column(db.String(16))
    phone = db.Column(db.String(16))

    def __repr__(self):
        return 'User:%s ' % self.name


class UserTools:

    def find(self, name='', phone='', user_id=''):

        if len(user_id) > 0:
            try:
                user = User.query.filter_by(user_id=user_id).first()
                print(user.user_id)
                return user

            except Exception as e:
                print(e)
                db.session.rollback()
                return api_request_type.user_cant_find_by_id
        elif len(name) > 0 and len(phone) > 0:
            try:
                user = User.query.filter_by(phone=phone).filter_by(name=name).first()
                print(user.user_id)
                return user

            except Exception as e:
                print(e)

                db.session.rollback()
                return api_request_type.user_cant_find
        else:
            return api_request_type.failure_no_pars


    def add(self, user_id, name, sex=None, phone=None):
        if len(name) > 0 and len(user_id) > 0:
            try:
                db.create_all()
                user1 = User(user_id=user_id, name=name, sex=sex, phone=phone)

                db.session.add(user1)
                db.session.commit()
            except Exception as e:
                print(e)
                print('增加出错')
                db.session.rollback()
        else:
            print('user_id 和 name 为空')

    def delete(self, user_id):

        try:
            user = User.query.filter_by(user_id=user_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            print('删除出错')
            db.session.rollback()


    def change(self):
        try:
            user = User.query.filter_by(name='10').filter_by(sex='男').first()
            user.name = '改了'
            db.session.commit()
        except Exception as e:
            print(e)
            print('更改出错')
            db.session.rollback()


    def deleteall(self):
        try:
            user = User.query.delete()
            db.session.commit()
        except Exception as e:
            print(e)
            print('删除出错')
            db.session.rollback()
