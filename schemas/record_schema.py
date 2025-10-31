from marshmallow import Schema, fields


class Record_Schema(Schema):
    temp = fields.Float(required=True)
    humidity = fields.Float(required=True)
    lux = fields.Float(required=True)
    soil_humid = fields.Float(required=True)
    timestamp = fields.Int(required=False)
    