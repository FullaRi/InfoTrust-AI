from marshmallow import Schema, fields, validate, ValidationError, validates

class PredictionSchema(Schema):
    user_input = fields.String(required=True, validate=validate.Length(min=10, max=1200))
