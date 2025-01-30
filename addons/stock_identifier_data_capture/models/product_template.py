from datetime import datetime
import random
from odoo import models, fields, api
from barcode import EAN13
import base64
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from PIL import Image

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_image = fields.Binary(string="Barcode Image", readonly=True)
    enable_barcode_feature = fields.Boolean(
        string="Enable Barcode Feature",
        compute="_compute_enable_barcode_feature"
    )

    @api.depends('enable_barcode_feature')
    def _compute_enable_barcode_feature(self):
        param = self.env['ir.config_parameter'].sudo().get_param('barcode_generator.enable_barcode_feature')
        for record in self:
            record.enable_barcode_feature = bool(param)

    def generate_barcode(self):
        self.ensure_one()
        barcode_type = self.env['ir.config_parameter'].sudo().get_param('barcode_generator.barcode_type', default='code128')
        self.barcode = self.generate_barcode_number(barcode_type)
        self.barcode_image = self.generate_barcode_image(barcode_type, self.barcode)

    def action_generate_barcode_for_selected(self):
        # Iterate over selected records and generate barcodes
        for record in self:
            record.generate_barcode()

    def generate_barcode_number(self, barcode_type):
        product_id = str(self.id)  # Use the product ID
        product_name = ''.join([c for c in self.name if c.isalnum()]).upper()[:3]
            
        if barcode_type == "code128":
            today_str = datetime.today().strftime('%Y%m%d')  # Get today's date in YYYYMMDD format
            barcode_number = f"RR-{today_str}/{product_id}"  # Use product ID in the sequence
            return barcode_number
        elif barcode_type == "code39":
            today_str = datetime.today().strftime('%Y%m')
            barcode_number = f"RR-{today_str}-{product_id}"  # Format: PR-PRODUCT_NAME-ID
            return barcode_number
        elif barcode_type == "ean13":
            return self.generate_ean13_barcode_sequence(product_id)
    
    def generate_ean13_barcode_sequence(self, product_id):
        date_str = datetime.today().strftime('%d%m%Y')
        date_str = f"{date_str[:4]}{date_str[6:]}"
        remaining_length = 12 - len(date_str)
        truncated_product_id = str(product_id)[:remaining_length]
        ean12 = f"{date_str}{truncated_product_id}".ljust(12, '0')
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

        # Get the checksum digit and form the full EAN-13 code
        checksum_digit = calculate_ean13_checksum(ean12)
        ean13 = f"{ean12}{checksum_digit}"

        return ean13

    def generate_barcode_image(self, barcode_type, barcode_number):


        buffer = BytesIO()
        barcode_cls = barcode.get_barcode_class(barcode_type)
        writer = ImageWriter()
        options = {
            'write_text': False,
            'module_width': 0.4,  # Adjust width of each bar
            'module_height': 15,  # Adjust height of each bar
            'quiet_zone': 1,  # Minimal space around the barcode
            'text_distance': 0,  # No distance for text
            'font_size': 10,  # Small text size
        }
        barcode_instance = barcode_cls(barcode_number, writer=writer)
        barcode_instance.write(buffer, options)
        
        # Resize the image
        buffer.seek(0)
        image = Image.open(buffer)
        width, height = image.size
        
        # Calculate new dimensions
        target_width = 500
        target_height = 150
        scale_width = target_width / width
        scale_height = target_height / height
        scale = min(scale_width, scale_height)  # Scale to maintain aspect ratio

        # Resize the image
        resized_image = image.resize((target_width, target_height), Image.ANTIALIAS)
        
        # Create a new image buffer for the resized image
        resized_buffer = BytesIO()
        resized_image.save(resized_buffer, format='PNG')
        resized_image_data = resized_buffer.getvalue()

        buffer.close()
        resized_buffer.close()
        
        return base64.b64encode(resized_image_data)
