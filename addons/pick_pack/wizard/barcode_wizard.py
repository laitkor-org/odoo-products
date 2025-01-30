from odoo import models, fields, api
import logging, json, base64

_logger = logging.getLogger(__name__)

class BarcodeWizard(models.TransientModel):
    _name = 'barcode.wizard'
    _description = 'Barcode Wizard'

    product_barcode_qty_ids = fields.One2many('barcode.wizard.line', 'wizard_id', string='Product Barcode Quantities')

    @api.model
    def default_get(self, fields):     
        res = super(BarcodeWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        active_ids = [int(id) for id in active_ids]
        _logger.info(f"Active IDs: {active_ids}")

        barcode_qty_lines = []
        products = self.env['product.template'].browse(list(map(int, active_ids)))

        for product in products:
            if len(product.product_variant_ids) > 1:
                product_variants = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
                for variant in product_variants:
                    attribute_values = variant.product_template_attribute_value_ids.mapped('name')
                    if(variant.combination_indices != ''):
                        barcode_qty_lines.append(
                        (0, 0, {
                            'product_id': product.id,
                            'barcode_qty': 1,
                            'variant_name':attribute_values,
                        }))
            else:
                barcode_qty_lines.append(
                    (0, 0, {
                        'product_id': product.id,
                        'barcode_qty': 1,
                        'variant_name':'',
                    })
                )
        res.update({
            'product_barcode_qty_ids': barcode_qty_lines,
        })
        return res
    

    def action_generate_barcode_pdf(self):
        _logger.info(f"Active IDs: {self.env.context.get('active_ids', [])}")
        
        product_quantities = {}
        
        for line in self.product_barcode_qty_ids:
            if not line.product_id or line.barcode_qty <= 0:
                _logger.error(f"Invalid line data: Product ID = {line.product_id}, Quantity = {line.barcode_qty}")
                continue
            
            _logger.info(f"Processing barcode wizard line: Product ID = {line.product_id.id}, Quantity = {line.barcode_qty}, Variant Name = {line.variant_name}")

            if line.variant_name:
                product_variants = self.env['product.product'].search([('product_tmpl_id', '=', line.product_id.id)])

                for variant in product_variants:
                    attribute_values = variant.product_template_attribute_value_ids.mapped('name')
                    variant_name_converted = line.variant_name.replace("'", '"')
                    variant_name_list = json.loads(variant_name_converted)
                    if(attribute_values == variant_name_list):
                        product_quantities[int(variant.id)] = {
                        "barcode_qty": line.barcode_qty,
                        "barcode_image": variant.barcode_image.decode('utf-8'),
                        "product_name": line.product_id.name,
                        "variant_name": line.variant_name,
                    }
            else:
                product_quantities[int(line.product_id.id)] = {
                        "barcode_qty": line.barcode_qty,
                        "barcode_image": line.product_id.barcode_image.decode('utf-8'),
                        "product_name": line.product_id.name,
                        "variant_name": '',
                    }
        
        _logger.info(f"Collected Barcode Quantities: {product_quantities}")
        
        return self.env.ref('pick_pack.barcode_report').report_action(
            self, data={'product_quantities': product_quantities}
        )

class BarcodeWizardLine(models.TransientModel):
    _name = 'barcode.wizard.line'
    _description = 'Barcode Wizard Line'

    wizard_id = fields.Many2one('barcode.wizard', string='Wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    barcode_qty = fields.Integer('Barcode Quantity', required=True, default=2)
    variant_name = fields.Char(string="Variant Name", required=False)
    @api.model
    def create(self, vals):
        if 'product_id' in vals:
            vals['product_id'] = int(vals['product_id'])
        _logger.info(f"Creating barcode wizard line with vals: {vals}")
        return super(BarcodeWizardLine, self).create(vals)