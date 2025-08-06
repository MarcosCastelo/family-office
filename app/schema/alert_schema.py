from marshmallow import Schema, fields

class AlertSchema(Schema):
    id = fields.Int(dump_only=True)
    family_id = fields.Int(required=True)
    asset_id = fields.Int(allow_none=True)
    tipo = fields.Str(required=True)
    mensagem = fields.Str(required=True)
    severidade = fields.Str(required=True)
    criado_em = fields.DateTime() 