from marshmallow import Schema, fields

#For api validations
class ItemSchema(Schema):
    name = fields.String(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)

class UpdateItemNameSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)

class LocationSchema(Schema):
    id = fields.Int(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)

class UpdateLocationSchema(Schema):
    id = fields.Int(required=True)
    position = fields.Int(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)
    
class SourceSchema(Schema):
    id = fields.Int(required=True)
    source = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

class PasswordSchema(Schema):
    id = fields.String(required=True)
    password = fields.String(required=True)