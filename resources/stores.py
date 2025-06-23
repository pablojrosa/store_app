from flask import request
import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModels

stores_blp = Blueprint("stores", __name__, description="Operations on stores")

@stores_blp.route("/store/<string:store_id>")
class Store(MethodView):
    @stores_blp.response(200, StoreSchema)
    def get(self,store_id):
        store = StoreModels.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        try:
            store = StoreModels.query.get_or_404(store_id)
            store_name = store.name
        except Exception as e:
            abort(404, message="Store not found. Error: " + str(e))
        try:
            db.session.delete(store)
            db.session.commit()
        except Exception as e:
            abort(500, message="An error occurred while deleting the store. Error: " + str(e))
        return {"message": "Store deleted", "name": store_name}, 200
    
@stores_blp.route("/stores")
class StoreList(MethodView):
    @stores_blp.response(201, StoreSchema(many=True))
    def get(self):
        stores = StoreModels.query.all()
        return stores
    
    @stores_blp.arguments(StoreSchema)
    def post(self,store_data):
        store = StoreModels(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")

        return store_data