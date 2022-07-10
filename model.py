from config import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storeName = db.Column(db.String(20), unique=True, nullable=False)

    barcodes = db.relationship('Barcode', backref='storeName', lazy=True)


class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), unique=True, nullable=False)
    menu = db.Column(db.String(20), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))


db.create_all()
