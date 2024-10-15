from odoo import models, fields, api

class ApiToken(models.Model):
    _name = 'api.token'
    _description = 'API Token'

    name = fields.Char(string='Token', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)

    @api.model
    def create_token(self, user):
        token = self.create({'name': self._generate_token(), 'user_id': user.id})
        return token.name

    def _generate_token(self):
        import secrets
        return secrets.token_hex(16)