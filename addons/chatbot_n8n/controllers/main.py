from odoo import http
from odoo.http import request

class ChatbotController(http.Controller):
    @http.route('/video-consultation', type='http', auth="public", website=True)
    def video_consultation(self):
        return request.render("chatbot_n8n.chatbot_n8n_ui")
