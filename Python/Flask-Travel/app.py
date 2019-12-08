from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        return 'User:%s ' % self.name


@app.route('/')
def hello_world():
    add(name='王5')
    add(name='王6', sex='女', phone=13333333333)
    return '123'

if __name__ == '__main__':
    app.run()

@app.route('/demo', methods=['GET'])
def demo():
      return {
        "error_code": 1,#要使用双引号，如果是单引号则运行时会报错，可以上网做在线json格式校验
        "stu_info": [
                {
                        "id": 309,
                        "name": "小白",
                        "sex": "男",
                        "age": 28,
                        "addr": "河南省济源市北海大道32号",
                        "grade": "天蝎座",
                        "phone": "18512572946",
                        "gold": 100
                },
                {
                        "id": 310,
                        "name": "小白",
                        "sex": "男",
                        "age": 28,
                        "addr": "河南省济源市北海大道32号",
                        "grade": "天蝎座",
                        "phone": "18516572946",
                        "gold": 100
                }
        ]
}
1

def add(name,sex = '未知',phone = '未知'):
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

def find():

    try:
        users = User.query.filter_by(name='10').filter_by(sex='男')
        for user in users:
            print(user.id)

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
