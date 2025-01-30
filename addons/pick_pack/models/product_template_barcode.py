from odoo import models, fields, api
from datetime import datetime
import barcode, logging
from barcode.writer import ImageWriter
import base64
from io import BytesIO

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        vals['barcode'] = vals.get('barcode', '')
        products = super(ProductTemplate, self).create(vals)        
        for product in products:
            barcode_sequence = self.generate_ean13_barcode_sequence(product.id,-1)
            product.barcode = barcode_sequence
            product._compute_barcode_image()
        return products
    
    def generate_ean13_barcode_sequence(self, product_id, variant_id):
        truncated_product_id = str(product_id)[:3]
        if variant_id == -1:
            relevant_digits = f"2024{truncated_product_id}"
        else:
            truncated_variant_id = str(variant_id)[:3]
            relevant_digits = f"2024{truncated_product_id}{truncated_variant_id}"
        ean12 = relevant_digits.ljust(12, '0')
        def calculate_ean13_checksum(ean12):
            total = 0
            for i, digit in enumerate(ean12):
                digit = int(digit)
                if i % 2 == 0:
                    total += digit
                else:
                    total += digit * 3
            checksum = (10 - (total % 10)) % 10
            return checksum
        checksum_digit = calculate_ean13_checksum(ean12)
        ean13 = f"{ean12}{checksum_digit}"

        return ean13

    def action_generate_barcode_for_all(self):
        all_products = self.env['product.template'].search([])

        for product in all_products:
            if len(product.product_variant_ids) > 1:
                for variant in product.product_variant_ids:
                    barcode_sequence = self.generate_ean13_barcode_sequence(product.id,variant.id)
                    variant.barcode = barcode_sequence
                    variant._compute_barcode_image()
            else:
                barcode_sequence = self.generate_ean13_barcode_sequence(product.id,-1)
                product.barcode = barcode_sequence
                product._compute_barcode_image()

    barcode_image = fields.Binary("Barcode Image", compute="_compute_barcode_image")

    @api.depends('barcode')
    def _compute_barcode_image(self):
        for product in self:
            if product.barcode:
                barcode_str = self._generate_barcode_image(product.barcode)
                product.barcode_image = base64.b64encode(barcode_str).decode('utf-8')
            else:
                product.barcode_image = False

    def _generate_barcode_image(self, barcode_value):
        barcode_class = barcode.get_barcode_class('ean13')
        barcode_instance = barcode_class(barcode_value, writer=ImageWriter())
        buffer = BytesIO()
        barcode_instance.write(buffer)
        
        return buffer.getvalue()

    def action_generate_barcode_pdf(self):
        return {
            'name': 'Generate Barcodes',
            'type': 'ir.actions.act_window',
            'res_model': 'barcode.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('pick_pack.view_barcode_wizard_form').id,
            'target': 'new',
            'context': {'active_ids': self.ids}
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        vals['barcode'] = vals.get('barcode', '')
        products = super(ProductProduct, self).create(vals)
        for product in products:
            barcode_sequence = self.generate_ean13_barcode_sequence(product.id,product.product_tmpl_id.id)
            product.barcode = barcode_sequence
            product._compute_barcode_image()

        return products
    
    def generate_ean13_barcode_sequence(self, product_id, variant_id):
        truncated_product_id = str(product_id)[:3]
        if variant_id == -1:
            relevant_digits = f"2024{truncated_product_id}"
        else:
            truncated_variant_id = str(variant_id)[:3]
            relevant_digits = f"2024{truncated_product_id}{truncated_variant_id}"
        ean12 = relevant_digits.ljust(12, '0')
        def calculate_ean13_checksum(ean12):
            total = 0
            for i, digit in enumerate(ean12):
                digit = int(digit)
                if i % 2 == 0:
                    total += digit
                else:
                    total += digit * 3
            checksum = (10 - (total % 10)) % 10
            return checksum
        checksum_digit = calculate_ean13_checksum(ean12)
        ean13 = f"{ean12}{checksum_digit}"

        return ean13

    barcode_image = fields.Binary("Barcode Image", compute="_compute_barcode_image")

    @api.depends('barcode')
    def _compute_barcode_image(self):
        for product in self:
            if product.barcode:
                barcode_str = self._generate_barcode_image(product.barcode)
                product.barcode_image = base64.b64encode(barcode_str).decode('utf-8')
            else:
                product.barcode_image = False
    
    def _generate_barcode_image(self, barcode_value):
        barcode_class = barcode.get_barcode_class('ean13')
        barcode_instance = barcode_class(barcode_value, writer=ImageWriter())
        buffer = BytesIO()
        barcode_instance.write(buffer)
        
        return buffer.getvalue()


class BarcodeReport(models.AbstractModel):
    _name = 'report.pick_pack.barcode_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        product_quantities = data.get('product_quantities', {})
        products = self.env['product.template'].browse(list(map(int, product_quantities.keys())))
        company = self.env.company
        return {
            'docs': products,
            'product_quantities': product_quantities,
            'company': company,
        }


