from . import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), index=True, unique=True)
    uri = db.Column(db.String)
    expires = db.Column(db.DateTime)
    delete_key = db.Column(db.String(32))
