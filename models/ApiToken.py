from odoo import models, fields

class AuthToken(models.Model):
    _name = 'auth.token'
    _description = 'Authentication Token'

    user_id = fields.Many2one('res.users', string='User', required=True)
    token = fields.Char(string='Token', required=True)