from odoo import http

class MyApiController(http.Controller):
    @http.route('/api/test', auth='none', type='http', methods=['GET'], csrf=False)
    def test_endpoint(self):
        print("Inside test endpoint method")
