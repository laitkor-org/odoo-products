from odoo import models, fields, api, http
from odoo.exceptions import AccessError
from odoo.http import request
import logging
from urllib.parse import urlparse

_logger = logging.getLogger(__name__)

class RatingRating(models.Model):
    _inherit = 'rating.rating'

    @api.model
    def create(self, vals):
        found = False
        # code that might be required for future references
        # referer_url = request.httprequest.headers.get('Referer')
        # if referer_url:
        #     parsed_url = urlparse(referer_url)
        #     current_path = parsed_url.path
        #     last_segment = current_path.split('/')[-1]
        #     product_slug = '-'.join(last_segment.split('-')[:-1])
        #     product_name = ' '.join(word for word in product_slug.split('-')).strip().lower()

        product = self.env['product.template'].browse(vals.get('res_id'))
        product_name = product.name.strip().lower()

        user = self.env.user
        if not user or user.id == self.env.ref('base.public_user').id:
            raise AccessError("You must be logged in to leave a review.")
        if not product_name:
            _logger.error("Product name could not be extracted from the URL")
            return request.redirect('/shop')
        
        email = user.partner_id.email
        related_partners = self.env['res.partner'].search([('email', '=', email)])
        related_partners_ids = related_partners.ids

        sale_order_lines = self.env['sale.order.line'].search([
            ('order_partner_id', 'in', related_partners_ids)
        ])

        product_ids = sale_order_lines.mapped('product_id')
        product_templates = product_ids.mapped('product_tmpl_id')

        product_template_names = [
            template.name.strip().lower() for template in product_templates if template.name
        ]

        _logger.info("Product to match: %s | Products in orders: %s", product_name, product_template_names)

        if product_name in product_template_names:
            found = True

        if not found:
            raise AccessError("You can only review products you have purchased.")
        else:
            return super(RatingRating, self).create(vals)
