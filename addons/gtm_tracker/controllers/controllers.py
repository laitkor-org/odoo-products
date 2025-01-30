# -*- coding: utf-8 -*-
# from odoo import http


# class GtmTracker(http.Controller):
#     @http.route('/gtm_tracker/gtm_tracker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gtm_tracker/gtm_tracker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gtm_tracker.listing', {
#             'root': '/gtm_tracker/gtm_tracker',
#             'objects': http.request.env['gtm_tracker.gtm_tracker'].search([]),
#         })

#     @http.route('/gtm_tracker/gtm_tracker/objects/<model("gtm_tracker.gtm_tracker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gtm_tracker.object', {
#             'object': obj
#         })

