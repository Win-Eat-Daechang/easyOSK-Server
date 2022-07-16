from flask import Flask, request, jsonify
from flask_cors import CORS

from config import app
from model import Store, Barcode, db

cors = CORS(app, resources={r'*': {'origins': '*'}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/code', methods=['GET'])
def get_code():
    store_id = request.args.get('store')
    menu_id = request.args.get('menu')
    if store_id and menu_id is not None:
        store = Store.query.filter(Store.id == store_id).first()
        if store is not None:
            barcode = Barcode.query.filter((Barcode.id == menu_id) & (Barcode.storeName == store)).first()
            if barcode is not None:
                return jsonify({"barcode": barcode.barcode}), 200
            else:
                return jsonify({'status': 'fail',
                                'message': '메뉴와 일치하는 바코드를 찾을 수 없습니다.'}), 404
        else:
            return jsonify({'status': 'fail',
                            'message': '일치하는 매장을 찾을 수 없습니다.'}), 404
    else:
        return jsonify({'status': 'fail',
                        'message': 'Invalid parameter inputs'}), 400


@app.route('/stores', methods=['GET'])
def get_available_stores():
    stores = Store.query.all()
    res = []
    for s in stores:
        if s.barcodes is not None:
            res.append({"id": s.id, "name": s.storeName})
    return jsonify(res)


@app.route('/stores/<int:store_id>', methods=['GET'])
def get_available_menus(store_id):
    storeid = store_id
    store = Store.query.filter(Store.id == storeid).first()
    if store is not None:
        menus = Barcode.query.filter(Barcode.storeName == store)
        res = []
        for m in menus:
            res.append({"id": m.id, "name": m.menu})
        return jsonify(res)
    else:
        return jsonify({'status': 'fail',
                        'message': '일치하는 매장을 찾을 수 없습니다.'}), 404


@app.route('/stores', methods=['POST'])
def create_store():
    storeName = request.json.get('storeName')
    store = Store(storeName=storeName)
    db.session.add(store)
    db.session.commit()
    res = []
    res.append({"id": store.id, "name": store.storeName})
    return jsonify(res), 201


@app.route('/menus', methods=['POST'])
def create_menu():
    storeid = request.json.get('storeId')
    barcode = request.json.get('barcode')
    menu = request.json.get('menu')
    store = Store.query.filter(Store.id == storeid).first()
    barcode = Barcode(barcode=barcode, menu=menu, storeName=store)
    db.session.add(barcode)
    db.session.commit()
    res = []
    res.append({"id": barcode.id, "name": barcode.menu, "barcode": barcode.barcode, "storeId": store.id})
    return jsonify(res), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
