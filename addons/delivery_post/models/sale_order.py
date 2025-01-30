# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import http
import os
from odoo.http import request
import logging, json
from ..controllers.controllers import DeliveryPost

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def generate_shipping_label(self):
        partner = self.partner_shipping_id

        state = partner.state_id
        state_name = state.name if state.name else None
        qr_code_image = os.getenv('ROOTSRAJA_QR_IMAGE', '')
        recipient_data = {
            "name" : partner.name if partner.name else None,
            "addressline1" : partner.street if partner.street else None,
            "addressline2" : partner.street2 if partner.street2 else None,
            "city" : partner.city if partner.city else None,
            "pincode" : partner.zip if partner.zip else None,
            "email" : partner.email if partner.email else None,
            "contact" : partner.phone or partner.mobile,
            "state" : state_name,
            "referenceid" : self.order_reference_india_post,
        }
        checkcity = self.getCityName(recipient_data["pincode"])
        logging.info("checking city for generating shiping label %s", checkcity)
        if checkcity == "local order":
            recipient_data["Label_city"] ="Lucknow"
            template_id="delivery_post.report_shipping_label_lucknow_pdf"
            return self.env.ref(template_id).with_context(qr_code_image=qr_code_image).report_action(self)

        delivery_post_controller = DeliveryPost()
        shippingLabelResponse = json.loads(delivery_post_controller.generateShippinglabel(self.order_reference_india_post, recipient_data, self.total_weight))
        if(shippingLabelResponse['success']):
            shippingLabel = shippingLabelResponse['payload'][0]['URL']
            self.shipping_label = shippingLabel
            self.write({'shipping_label': self.shipping_label})
            logging.info("Generated Shipping Label %s", shippingLabel)
        else:
            shippingLabel = shippingLabelResponse['error']
            logging.info("Shipping Label couldn't be generated : %s", shippingLabel)
