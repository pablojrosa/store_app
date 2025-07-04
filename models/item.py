from db import db


class ItemModels(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    store_id= db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store=db.relationship('StoreModels', back_populates='items')
    