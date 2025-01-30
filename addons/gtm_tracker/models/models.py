from odoo import models, fields

class GTMTracker(models.Model):
    _name = 'gtm.tracker'
    _description = 'GTM Tracker'

    name = fields.Char(string='Name', required=True)