import json
import secrets
from odoo import http
from odoo.http import request


class MyApiController(http.Controller):
    @http.route('/v1/auth/login', methods=["POST"], type="http", auth="none", csrf=False)
    def login(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        username = vals.get('username')
        password = vals.get('password')

        # Utiliser la méthode authenticate pour vérifier les identifiants
        uid = request.session.authenticate(request.db, username, password)

        if uid:
            # Récupérer l'utilisateur
            user = request.env['res.users'].sudo().browse(uid)

            # Générer un token
            token = secrets.token_hex(16)

            # Créer ou mettre à jour le token pour l'utilisateur
            request.env['auth.token'].sudo().create({
                'user_id': user.id,
                'token': token,
            })
            return request.make_json_response({
                "message": "Login successful",
                "token": token
            }, status=200)
        else:
            return request.make_json_response({
                "message": "Invalid credentials"
            }, status=401)

