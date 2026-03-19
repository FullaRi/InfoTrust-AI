from marshmallow import Schema, fields, validate, ValidationError, validates
from utils import ml


ACCEPTED_DETECTION_TYPES = [ml.DETECTION_TYPE_DEEP_LEARNING, ml.DETECTION_TYPE_AI_AGENT, ml.DETECTION_TYPE_AI_AGENT__DEEP_LEARNING]


class FactCheckingSchema(Schema):
    user_input = fields.String(required=True, validate=validate.Length(min=10, max=500))
    detection_type = fields.String(required=True, validate=validate.OneOf(ACCEPTED_DETECTION_TYPES))
