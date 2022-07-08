from flask import Flask, request
import pymysql


app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/code', methods=['POST'])
def get_code():
    params = request.json.get('string')
    store, menu =params.split(' ')
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
