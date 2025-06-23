from flask import request
import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import ItemSchema, UpdateItemSchema
from models import ItemModels
from sqlalchemy.exc import SQLAlchemyError
from db import db
items_blp = Blueprint("items", __name__, description="Operations on items")

@items_blp.route("/items/<string:item_id>")
class Items(MethodView):
    @items_blp.response(200, ItemSchema)
    def get(self,item_id):
        try:
            print("item_id", item_id)   
            item = ItemModels.query.get_or_404(item_id)
        except Exception as e:
            abort(404, message="Item not found. Error: " + str(e))
        return item
    
    @items_blp.arguments(UpdateItemSchema)
    @items_blp.response(200, ItemSchema)
    def put(self,item_data, item_id):
        item = ItemModels.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModels(id=item_id, **item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item")

        return item

    def delete(self,item_id):
        try:
            item = ItemModels.query.filter_by(id=item_id).first()
            item_name = item.name
        except Exception as e:
            abort(404, message="Item not found. Error: " + str(e))
        try:
            db.session.delete(item)
            db.session.commit()
        except Exception as e:
            abort(500, message="An error occurred while deleting the item. Error: " + str(e))
        return {"message": "Item deleted", "name": item_name}, 200
    


@items_blp.route("/items")
class GetItems(MethodView):
    @items_blp.response(201, ItemSchema(many=True))
    def get(self):
        items = ItemModels.query.all()
        return items
    
    @items_blp.arguments(ItemSchema)
    @items_blp.response(201, ItemSchema)
    def post(self, item_data): 
        item = ItemModels(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Error general de base de datos. Error: " + str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, message="Error inesperado al insertar el item.")
    
        return item