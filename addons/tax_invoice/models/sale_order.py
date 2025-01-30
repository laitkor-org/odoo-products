from odoo import models, fields, api
import requests, logging, os
from dotenv import load_dotenv 
load_dotenv()
import pgeocode
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    same_state = fields.Boolean(string="API State Name", compute="_compute_api_state_name", store=True)
    
    # @api.depends('partner_id.zip')
    def _compute_api_state_name(self):
        nomi = pgeocode.Nominatim('IN')
        for record in self:
            admin_user = self.env['res.users'].browse(2)
            admin_zip = admin_user.partner_id.zip
            if record.partner_id.zip and admin_zip:
                    # Query state names using postal codes
                    response1 = nomi.query_postal_code(record.partner_id.zip)
                    response2 = nomi.query_postal_code(admin_zip)

                    # Extract state names if responses is valid and not null
                    state_name1 = response1.state_name if response1 is not None and not response1.empty else None
                    state_name2 = response2.state_name if response2 is not None and not response2.empty else None
                
                    if state_name1 and state_name2:
                       record.same_state = state_name1 == state_name2
                       logging.info("State names of user and admin are valid: %s, %s", state_name1, state_name2)
                    else:
                       record.same_state = False
                       logging.warning("Invalid state names: state_name1=%s, state_name2=%s", state_name1, state_name2)
                   
            else:
                    record.same_state = False

    def call_pincode_api_and_generate_invoice(self):
        self._compute_api_state_name()
        return self.action_generate_tax_invoice()

    def action_generate_tax_invoice(self):
        return self.env.ref('tax_invoice.report_sale_tax_invoice_pdf').report_action(self)
    
    tax_number = fields.Char(
        string="Tax Number",
        copy=False, index=True,
        help="Sequential number assigned when the order is confirmed.",
    )

    @api.model
    def _get_next_tax_number(self):
        """Compute the next tax number based on the max current value."""
        last_order = self.search(
            [('tax_number', '!=', False), ('state', '=', 'sale')],
            order="date_order DESC",
            limit=1)
        if last_order:
            last_number = last_order.tax_number
            parts = last_number.split('-')
            if len(parts) == 3:
                current_year = datetime.now().year
                sequence_number = int(parts[2])
                new_sequence_number = f"{sequence_number + 1:06d}"
                return "INV-LCS"+str(current_year)+"-"+new_sequence_number
        else:
            logging.info("Last order not found!")
        return ""

    def action_confirm(self):
        """Override the confirmation method to assign the tax number."""
        for order in self:
            order.tax_number = self._get_next_tax_number()
        return super(SaleOrder, self).action_confirm()

