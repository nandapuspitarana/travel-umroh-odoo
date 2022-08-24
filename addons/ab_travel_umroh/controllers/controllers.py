# -*- coding: utf-8 -*-
# from odoo import http


# class AbTravelUmroh(http.Controller):
#     @http.route('/ab_travel_umroh/ab_travel_umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ab_travel_umroh/ab_travel_umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ab_travel_umroh.listing', {
#             'root': '/ab_travel_umroh/ab_travel_umroh',
#             'objects': http.request.env['ab_travel_umroh.ab_travel_umroh'].search([]),
#         })

#     @http.route('/ab_travel_umroh/ab_travel_umroh/objects/<model("ab_travel_umroh.ab_travel_umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ab_travel_umroh.object', {
#             'object': obj
#         })
