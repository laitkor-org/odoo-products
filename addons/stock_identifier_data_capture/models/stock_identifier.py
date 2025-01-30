import base64
from io import BytesIO
import os
import tempfile
from venv import logger
import qrcode
from odoo import models, fields, api
from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter

class AccountMove(models.Model):
    _inherit = 'account.move'

    qr_code = fields.Binary(string='QR Code', readonly=True)
    
    def generate_qr_code(self):
        logger.info('Generate QR Code method called for record ID %s', self.id)
        self.qr_code=False
        for record in self:
            # record.qr_code = False
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            data = (
                f"Invoice ID: {record.id}\n"
                f"Customer: {record.partner_id.name}\n"
                f"Invoice Date: {record.invoice_date}\n"
                f"Delivery Address: {record.partner_shipping_id.name}\n"
                f"Payment Term: {record.invoice_payment_term_id.name}\n"
                # f"Date: {record.invoice_date}\n"
                # f"Amount: {record.amount_total}\n"
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save QR Code Image to BytesIO
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            # img_data = base64.b64encode(img_buffer.getvalue())
            img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            # Store QR Code in the record
            record.qr_code = img_data

#######################  For generate every product's QR code #########################

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qr_code = fields.Binary(string='QR Code', readonly=True)

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        record.generate_qr_code()
        return record

    def write(self, vals):
        print(vals)
        res = super(ProductTemplate, self).write(vals)
        if 'name' in vals or 'list_price' in vals:
            self.generate_qr_code()
        return res

    def generate_qr_code(self):
        for record in self:
            quants = self.env['stock.quant'].search([('product_id', '=', record.id)])
            total_quantity = sum(quant.quantity for quant in quants)
            locations = ', '.join(set(quant.location_id.name for quant in quants))
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            data = (
                f"Product ID: {record.id}\n"
                f"Product Name: {record.name}\n"
                f"Product Price: {record.list_price}\n"
                f"Total Quantity: {total_quantity}\n"
                f"Locations: {locations}\n"
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save QR Code Image to BytesIO
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            img_data = base64.b64encode(img_buffer.getvalue())

            # Store QR Code in the record
            record.qr_code = img_data

class PaperSizeWizard(models.TransientModel):
    _name = 'paper.size.wizard'
    _description = 'Paper Size Wizard'

    paper_size = fields.Selection([
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('Letter', 'Letter')
    ], string='Paper Size', required=True, default='A4')

    @api.model
    def default_get(self, fields):
        res = super(PaperSizeWizard, self).default_get(fields)
        active_ids = self.env.context.get('default_order_ids', [])
        res['order_ids'] = [(6, 0, active_ids)]
        return res


    order_ids = fields.Many2many('sale.order', string='Orders')

    def generate_report(self):
        self.ensure_one()
        paper_format_map = {
            'A4': 'stock_identifier_data_capture.report_shipping_label_action1',
            'A5': 'stock_identifier_data_capture.report_shipping_label_action2',
            'Letter': 'stock_identifier_data_capture.report_shipping_label_action',
        }
        # report_action = self.env.ref('stock_identifier_data_capture.report_shipping_label_action').report_action(self)
        report_action_ref = paper_format_map.get(self.paper_size)
        
        if not report_action_ref:
            raise ValueError("Invalid paper size selected.")
        
        # Get the report action reference
        report_action = self.env.ref(report_action_ref).report_action(self)
        return report_action
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def action_open_popup(self):
    #     return {
    #         'name': 'Shipping Label',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'paper.size.wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {
    #             'default_order_ids': self.ids,
    #         },
    #     }
    def action_open_popup(self):
        action = self.env.ref('stock_identifier_data_capture.action_shipping_label_wizard').read()[0]
        action['context'] = {
            'default_order_ids': self.ids,
        }
        return action
