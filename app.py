from flask import Flask, request, jsonify

from config import app
from model import Store, Barcode, db


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/code', methods=['POST'])
def get_code():
    store = request.json.get('매장')
    menu = request.json.get('메뉴')
    store = Store.query.filter(Store.storeName == store).first()
    if store is not None:
        barcode = Barcode.query.filter((Barcode.menu.like(menu)) & (Barcode.storeName == store)).first()
        if barcode is not None:
            return jsonify({"barcode": barcode.barcode}), 201
        else:
            return jsonify({ 'status': 'fail',
                    'message': '메뉴와 일치하는 바코드를 찾을 수 없습니다.'}), 401
    else:
        return jsonify({'status': 'fail',
                        'message': '일치하는 매장을 찾을 수 없습니다.'}), 401


@app.route('/stores', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    res = []
    for s in stores:
        res.append(s.storeName)
    return jsonify(res)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
