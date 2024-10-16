import json
from odoo import http, _
from odoo.http import request

def get_user_from_token(token):
    token_record = request.env['auth.token'].sudo().search([('token', '=', token)])
    return token_record.user_id if token_record else None

def authenticate_request():
    token = request.httprequest.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
        user = get_user_from_token(token)
        if user:
            print(user)
            return user
        return None
    print("pas de token")
    return None

def valid_response(data, status):
    response_body={
        'message':'Success',
        'data':data
    }
    return request.make_json_response(response_body, status=status)

class PropertyApi(http.Controller):

    @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": _("Please, name fields cannot be empty")
            }, status=400)
        try:
            res = request.env['estate.property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": _("Property has been created successfully")
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)

    @http.route('/v1/property/json', methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['estate.property'].sudo().create(vals)
        if res:
            return [{
                "message": _("Property has been created successfully"),
                "id": res.id,
                "name": res.name,
            }]

    @http.route('/v1/property/<int:property_id>', methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['estate.property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Id do not exist"
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": _("Property has been modify successfully")
            }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)

    @http.route('/v1/property/<int:property_id>', methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['estate.property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "ID  does not exist!"
                }, status=400)
            return request.make_json_response({
                "id": property_id.id,
                "quantity":property_id.quantity,
                "unit_price":property_id.unit_price,
                "name": property_id.name
            }, status=400)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            })

    @http.route('/v1/property/<int:property_id>', methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id=request.env['estate.property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error":"ID does not exist!",
                },status=400)
            property_id.unlink()
            return request.make_json_response({
                "id":"Property has been deleted",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "id": error,
            }, status=400)

    @http.route('/v1/properties', methods=["GET"], type="http", auth="user", csrf=False)
    def get_properties_list(self):
        try:
            user = authenticate_request()
            if not user:
                return request.make_json_response({
                    "message": "Unauthorized"
                }, status=401)

            # Récupérer les paramètres de pagination depuis la requête
            page = int(request.httprequest.args.get('page', 1))  # Page par défaut = 1
            limit = int(request.httprequest.args.get('limit', 10))  # Limite par défaut = 10

            # Calculer l'offset
            offset = (page - 1) * limit

            # Récupérer les propriétés avec pagination
            properties_ids = request.env['estate.property'].search([], offset=offset, limit=limit)
            total_properties = request.env['estate.property'].search_count([])  # Nombre total d'enregistrements

            if not properties_ids:
                return request.make_json_response({
                    "message": "There are no records!"
                }, status=404)

            # Retourner les propriétés avec le total et la pagination
            return valid_response({
                "total": total_properties,
                "page": page,
                "limit": limit,
                "properties": [{
                    "id": property_id.id,
                    "quantity": property_id.quantity,
                    "unit_price": property_id.unit_price,
                    "name": property_id.name
                } for property_id in properties_ids]
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "message": str(error),
            }, status=400)

    @http.route('/v1/auth/logout', methods=["POST"], type="http", auth="user", csrf=False)
    def logout(self):
        user = authenticate_request()
        if user is None:
            return request.make_json_response({
                "message": "Unauthorized"
            }, status=401)
        else:
            token = request.httprequest.headers.get('Authorization')
            auth_token = request.env['auth.token'].sudo().search([('token', '=', token.split(' ')[1])])
            auth_token.sudo().unlink()
            request.session.logout()
            return request.make_json_response({
                "message": "Logout successful"
            }, status=200)