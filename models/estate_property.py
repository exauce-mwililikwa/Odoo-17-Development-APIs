from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a model of estate property"

    name = fields.Char(string="name of house", required=True)
    quantity = fields.Integer(required=True)
    unit_price = fields.Integer(required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the town must be unique!'),
    ]
