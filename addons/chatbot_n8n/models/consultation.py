from odoo import models, fields,http
from odoo.http import request

class ConsultationRequest(models.Model):
    _name = "consultation.request"
    _description = "Video Consultation Request"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Contact Number", required=True)
    message = fields.Text(string="Message")
    pricing_plan = fields.Selection([
        ('100', '₹100'),
        ('500', '₹500'),
    ], string="Pricing Plan", required=True)
    consultation_date = fields.Datetime(string="Consultation Date", required=True)
    time_slot = fields.Selection([
        ('2-3', '2-3 PM'),
        ('3-4', '3-4 PM'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ], string="Time Slot", required=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Payment Status", default="pending")


class WebsiteCustomController(http.Controller):
    @http.route('/video-consultation',type='http', auth='public', website=True)
    def video_consultation_page(self,**kwargs):
        return request.render('chatbot_n8n.chatbot_n8n_ui')
