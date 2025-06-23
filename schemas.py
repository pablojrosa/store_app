from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    item_id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    store_id = fields.String(dump_only=True)
    name = fields.String(required=True)

class UpdateItemSchema(Schema):
    name = fields.String()
    price = fields.Float()
    store_id = fields.Integer()

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)