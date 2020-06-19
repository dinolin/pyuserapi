from marshmallow import Schema, fields, ValidationError, pre_load

# Custom validator
def must_not_be_blank(data):
	if not data:
		raise ValidationError('Data not provided.')


class RoleSchema(Schema):
	id = fields.Int(dump_only = True)
	name = fields.Str(required = True, validate = must_not_be_blank)
	description = fields.Str()


class UserSchema(Schema):
	id = fields.Int(dump_only = True)
	username = fields.Str()
	email = fields.Str()
	password = fields.Str()
	age = fields.Int()
	country = fields.Str()
	hobbies = fields.Str()
	active = fields.Boolean()
	confirmed_at = fields.DateTime(allow_none = True)
	roles = fields.Nested(RoleSchema, many = True, only = 'name')



