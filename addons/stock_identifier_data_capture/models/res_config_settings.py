from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    barcode_type = fields.Selection([
        ('code128', 'Code 128'),
        ('code39', 'Code 39'),
        ('ean13', 'EAN 13'),
    ], string='Barcode Type', default='code128', config_parameter='barcode_generator.barcode_type')

    enable_barcode_feature = fields.Boolean(string="Enable Barcode Feature", config_parameter='barcode_generator.enable_barcode_feature')
