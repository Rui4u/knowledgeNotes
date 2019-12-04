from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


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