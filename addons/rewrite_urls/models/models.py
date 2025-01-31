# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class rewrite_urls(models.Model):
    _name = 'rewrite_urls.rewrite_urls'
    _description = 'SEO Friendly URL'

    name = fields.Char('Name')
    original_url = fields.Char('Original URL', required=True)
    seo_friendly_url = fields.Char('SEO-Friendly URL', required=True)
    fetch_content = fields.Boolean(string="Fetch Content Instead of Redirecting", default=False)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now)
    @api.constrains('seo_friendly_url')
    def _check_seo_friendly_url(self):
        for record in self:
            if not re.match(r'^[a-zA-Z0-9-_\/]+$', record.seo_friendly_url):
                raise ValidationError(
                    'An SEO-friendly URL must only contain lowercase letters, uppercase letters, numbers, hyphens, underscores and forward slashes.'
                )
            
            existing_seo = self.search([('seo_friendly_url', '=', record.seo_friendly_url), ('id', '!=', record.id)], limit=1)
            if existing_seo:
                raise ValidationError('This SEO-friendly URL already exists.')

            existing_original = self.search([('original_url', '=', record.original_url), ('id', '!=', record.id)], limit=1)
            if existing_original:
                raise ValidationError('This original URL already exists.')

