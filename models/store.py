from db import db

class StoreModels(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship('ItemModels', back_populates='store', lazy='dynamic', cascade="all, delete")