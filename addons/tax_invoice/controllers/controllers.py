# -*- coding: utf-8 -*-
# from odoo import http


# class TaxInvoice(http.Controller):
#     @http.route('/tax_invoice/tax_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_invoice/tax_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_invoice.listing', {
#             'root': '/tax_invoice/tax_invoice',
#             'objects': http.request.env['tax_invoice.tax_invoice'].search([]),
#         })

#     @http.route('/tax_invoice/tax_invoice/objects/<model("tax_invoice.tax_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_invoice.object', {
#             'object': obj
#         })

