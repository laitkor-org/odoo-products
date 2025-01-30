# -*- coding: utf-8 -*-
# from odoo import http


# class UpdateEmailTemplate(http.Controller):
#     @http.route('/update_email_template/update_email_template', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/update_email_template/update_email_template/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('update_email_template.listing', {
#             'root': '/update_email_template/update_email_template',
#             'objects': http.request.env['update_email_template.update_email_template'].search([]),
#         })

#     @http.route('/update_email_template/update_email_template/objects/<model("update_email_template.update_email_template"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('update_email_template.object', {
#             'object': obj
#         })

