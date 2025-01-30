# -*- coding: utf-8 -*-
import requests,logging,os,json
from odoo import http
from odoo.http import request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import pytz

from dotenv import load_dotenv 
load_dotenv()

_logger = logging.getLogger(__name__)

# constant values
TRACKING_SUCCESS_PAGE = "/trackingSuccess"
TRACKING_FAILURE_PAGE = "/trackingFailure"
ORDER_TRACKING_PAGE = "/trackOrderPage"
ORDER_TRACKING_ENDPOINT = "/track"
PINCODE_FETCHING_ENDPOINT = '/api/deliveryPincode'
ORDER_SUCCESS_ENDPOINT = "/api/orderSuccess"
TARIFF_CALCULATION_ENDPOINT = '/api/getDeliveryCharges'
POD_ACK_FLAG = "No"
VPP_VALUE = 0
PROOF_OF_DELIVERY_FLAG = False
INS_VALUE = 0
SERVICE = "SP"
ARTICLE_LENGTH = 17.15
ARTICLE_WIDTH = 17.15
ARTICLE_HEIGHT = 60.96
COD_VALUE = 0
CITY = "Lucknow"
COUNTRY = "India"

class DeliveryPost(http.Controller):
    def generateAccessToken(self):
        url = os.getenv('INDIA_POST_ACCESS_TOKEN_API_URL')
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "username": os.getenv('USERNAME'),
            "password": os.getenv('PASSWORD'),
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            return {'status_code': response.status_code, 'data': json_response}
        except requests.exceptions.RequestException as e:
            status_code = response.status_code if response is not None else None
            return {'status_code': status_code, 'error': str(e)}
        
    @http.route(ORDER_TRACKING_PAGE, auth='user', methods=['GET'], website=True, csrf=False)
    def renderTrackingPage(self, **kw):
        return request.render('delivery_post.page_template_delivery')

    @http.route(ORDER_TRACKING_ENDPOINT, type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def track_consignment(self, **post):
        consignment_number = post.get('consignment_number')
        url = os.getenv('ORDER_TRACKING_URL')
        try:
            response = requests.post(url, data={'consignment_number': consignment_number})
            _logger.info("Tracking order with consignment number : %s", consignment_number)
            if response.status_code == 200:
                data = response.json()
                table_summary = data.get('tracking_table_summary')
                table_details = data.get('tracking_table_details')
                return request.redirect('/trackingSuccess?summary=%s&details=%s' % (table_summary, table_details))
            else:
                return request.redirect('/trackingFailure')
        except Exception as e:
            return request.redirect('/trackingFailure')

    @http.route(TRACKING_SUCCESS_PAGE, auth='user', website=True)
    def tracking_success(self, **kw):
        summary = kw.get('summary')
        details = kw.get('details')
        return request.render('delivery_post.tracking_success', {
            # 'table_summary': summary,
            'table_details': details
        })
    
    @http.route(TRACKING_FAILURE_PAGE, auth='user', website=True)
    def tracking_failure(self):
        return request.render('delivery_post.tracking_failure')

    @http.route(PINCODE_FETCHING_ENDPOINT, auth='public', methods=['POST'], csrf=False)
    def pincode_delivery(self, **post):
        try:
            request_data = json.loads(http.request.httprequest.data.decode('utf-8'))
            pincode = request_data.get('pincode')
            accessTokenResponse = self.generateAccessToken()
            if(accessTokenResponse.get('status_code') == 200):
                accessToken = accessTokenResponse.get('data').get('access_token')
            else:
                accessToken = None
                return http.request.make_response(json.dumps({"success": False, "error": "Unable to generate access token", "category":"Access Token API"}), headers={'Content-Type': 'application/json'})
            url = os.getenv('INDIA_POST_PINCODE_VALIDATION_API_URL')
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {accessToken}",
            }
            data = {
                "Input_Pincode":pincode,
                }
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                json_response = response.json()
            except requests.exceptions.RequestException as e:
                return http.request.make_response(json.dumps({"success": False, "error": str(e)}),
                headers={'Content-Type': 'application/json'}
            )
            finally:
                return http.request.make_response(json.dumps({"success": True, "error": "no errors", "result":json_response}),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            error_message = str(e)
            return http.request.make_response(
                json.dumps({"success": False, "error": error_message}),
                headers={'Content-Type': 'application/json'}
            )
        
    # def fetch_pincode_data(self, pincode):
    #     try:
    #         accessTokenResponse = self.generateAccessToken()
    #         if accessTokenResponse.get('status_code') == 200:
    #             accessToken = accessTokenResponse.get('data').get('access_token')
    #         else:
    #             return http.request.make_response(
    #                 json.dumps({"success": False, "error": "Unable to generate access token", "category": "Access Token API"}),
    #                 headers={'Content-Type': 'application/json'}
    #             )
    #         url = os.getenv('INDIA_POST_PINCODE_VALIDATION_API_URL')
    #         headers = {
    #             'Content-Type': 'application/json',
    #             'Authorization': f"Bearer {accessToken}",
    #         }
    #         data = {"Input_Pincode": pincode}
    #         try:
    #             response = requests.post(url, headers=headers, json=data)
    #             response.raise_for_status()
    #             json_response = response.json()
    #             return json_response
    #         except requests.exceptions.RequestException as e:
    #             return e
    #     except Exception as e:
    #         return e


    @http.route(TARIFF_CALCULATION_ENDPOINT, auth='public', methods=['POST'], csrf=False)
    def get_delivery_charge(self, **post):
        try:
            request_data = json.loads(http.request.httprequest.data.decode('utf-8'))
            total_weight = request_data.get('total_weight')
            destinationPincode = request_data.get('destinationPincode')
            url = os.getenv('INDIA_POST_TARIFF_API_URL')
            barcode=os.get
            headers = {
                'Content-Type': 'application/json',
            }
            data = [
            {
                "service": SERVICE,
                "sourcepin": os.getenv('SOURCE_PINCODE'),
                "destinationpin": destinationPincode,
                "weight": total_weight*1000,
                "length": ARTICLE_LENGTH,
                "breadth": ARTICLE_WIDTH,
                "height": ARTICLE_HEIGHT,
                "POD_ACK_Flag": POD_ACK_FLAG,
                "VPP_Value" : VPP_VALUE,
                "INS_Value": INS_VALUE,
                "COD_Value": COD_VALUE,
            }]
            logging.info("data i want to log %s", data)
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                json_response = response.json()
                return http.request.make_response(
                        json.dumps({"success": True, "json_response": json_response}),
                        headers={'Content-Type': 'application/json'}
            )
            except requests.exceptions.RequestException as e:
                return http.request.make_response(json.dumps({"success": False, "error": str(e)}),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            error_message = str(e)
            return http.request.make_response(
                json.dumps({"success": False, "error": error_message}),
                headers={'Content-Type': 'application/json'}
            )

    @http.route(ORDER_SUCCESS_ENDPOINT, auth='public', methods=['POST'], csrf=False)
    def order_successful(self, **post):
        try:
            request_data = json.loads(http.request.httprequest.data.decode('utf-8'))
            recipient_data = request_data.get('recipient_data')
            orderID = request_data.get('orderID')
            order = request.env['sale.order'].sudo().search([('name', '=', orderID)], limit=1)
            order_weight = order.total_weight
            accessTokenResponse = self.generateAccessToken()
            if(accessTokenResponse.get('status_code') == 200):
                accessToken = accessTokenResponse.get('data').get('access_token')
            else:
                accessToken = None
                return http.request.make_response(json.dumps({"success": False, "error": "Unable to generate access token"}), headers={'Content-Type': 'application/json'})
            articleID = self.generateArticleNumber()
            # self.outboundTracking()
            shippingLabelResponse = json.loads(self.generateShippinglabel(articleID, recipient_data, order_weight))
            shippingLabel = None
            if(shippingLabelResponse['success']):
                shippingLabel = shippingLabelResponse['payload'][0]['URL']
            else:
                shippingLabel = shippingLabelResponse['error']
                return http.request.make_response(json.dumps({"success": False, "error": shippingLabel,"category":"Label API"}), headers={'Content-Type': 'application/json'})
            
            presentDate = datetime.now(pytz.utc)
            iso_format_date = presentDate.isoformat()
            if(recipient_data.get('name')):
                data = [{
                "identifier": os.getenv('IDENTIFIER'),
                "articleid": articleID,
                "articletype": SERVICE,
                "articlelength": ARTICLE_LENGTH,
                "articlewidth": ARTICLE_WIDTH,
                "articleheight": ARTICLE_HEIGHT,
                "articleweight": order_weight*1000,
                "codvalue": COD_VALUE,
                "insurancevalue": INS_VALUE,
                "proofofdeliveryflag": PROOF_OF_DELIVERY_FLAG,
                "customerid": os.getenv('CUSTOMER_ID'),
                "contractnumber": os.getenv('CONTRACT_ID'),
                "sendername": os.getenv('SENDER_NAME'),
                "senderaddressline1": os.getenv('SENDER_ADDRESS_LINE1'),
                "senderaddressline2": os.getenv('SENDER_ADDRESS_LINE2'),
                "senderaddressline3": os.getenv('SENDER_ADDRESS_LINE3'),
                "sendercity": CITY,
                "senderpincode": os.getenv('SOURCE_PINCODE'),
                "sendercountry": COUNTRY,
                "senderemail": os.getenv('SENDER_EMAIL'),
                "sendermobile": os.getenv('SENDER_MOBILE'),
                "nameofreceipient": recipient_data.get('name'),
                "receipientaddressline1": recipient_data.get('addressline1'),
                "receipientaddressline2": recipient_data.get('addressline2'),
                "receipientaddressline3": "",
                "receipientcity": recipient_data.get('city'),
                "receipientpincode": recipient_data.get('pincode'),
                "receipientcountry": COUNTRY,
                "receipientemail": recipient_data.get('email'),
                "receipientmobile": recipient_data.get('contact'),
                "refid": recipient_data.get('referenceid'),
                }]
                url = os.getenv('INDIA_POST_BOOKING_API_URL')
                headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f"Bearer {accessToken}",
                        'x-request-id': os.getenv('X-REQUEST-ID'),
                        'date': iso_format_date,
                        }
                try:
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    json_response = response.json()
                    return http.request.make_response(json.dumps({"success": True, "payloadBooking": json_response[0]['articleid'], "payloadShipping": shippingLabel}), headers={'Content-Type': 'application/json'})
                except requests.exceptions.RequestException as e:
                    return http.request.make_response(json.dumps({"success": False, "error": str(e), "payloadShipping": shippingLabel,"category":"Booking API"}),
                    headers={'Content-Type': 'application/json'}
                )
        except Exception as e:
            return http.request.make_response(
                json.dumps({"success": False, "error": str(e), "payloadShipping": shippingLabel,"category":"Booking API"}),
                headers={'Content-Type': 'application/json'}
            )


    def generateShippinglabel(self, article_id, recipient_data, order_weight):
        try:
            data = {
                "ArticleNumber": article_id,
                "service": SERVICE,    
                "SenderName": os.getenv('SENDER_NAME'),
                "SenderAddressLine1": os.getenv('SENDER_ADDRESS_LINE1'),
                "SenderAddressLine2": os.getenv('SENDER_ADDRESS_LINE2'),
                "SenderAddressLine3": os.getenv('SENDER_ADDRESS_LINE3'),
                "SenderCity": CITY,
                "SenderPincode": os.getenv('SOURCE_PINCODE'),
                "SenderMobile": os.getenv('SENDER_MOBILE'),
                "NameOfReceipient": recipient_data.get('name'),
                "ReceipientAddressLine1": recipient_data.get('addressline1'),
                "ReceipientAddressLine2": recipient_data.get('addressline2'),
                "ReceipientAddressLine3": "",
                "ReceipcientCity": recipient_data.get('city'),
                "ReceipientMobile": recipient_data.get('contact'),
                "ReceipientCountry": COUNTRY,
                "ReceipientPincode": recipient_data.get('pincode'),
                "ReceipientState": recipient_data.get('state'),
                "articleweight": order_weight*1000,
                "length": ARTICLE_LENGTH,
                "breadth": ARTICLE_WIDTH,
                "height": ARTICLE_HEIGHT,
                "BillerId": os.getenv('BILLER_ID'),
                "InsuredValue":INS_VALUE,
                "CodValue" :COD_VALUE,
                "VPPValue" : VPP_VALUE,
            }
            url = os.getenv('INDIA_POST_LABEL_API_URL')
            headers = {
                'Content-Type': 'application/json',
            }
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                json_response = response.json()
                return json.dumps({'success': True, 'payload': json_response})
            except requests.exceptions.RequestException as e:
                return json.dumps({"success": False, "error": str(e)})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
        
    def generateArticleNumber(self):
        company = request.env['res.company'].sudo().browse(1)
        if SERVICE == "BP":
            fixed_consignment_number = company.barcode_series_bp
            prefix_code = "CU"
        elif SERVICE == "SP":
            fixed_consignment_number = company.barcode_series_sp
            prefix_code = "EZ"
        postfix_code = "IN"
        number_to_update = fixed_consignment_number
        number_weight_factors = os.getenv('WEIGHT_FACTORS')
        sum_of_products = 0
        for j in range(0,8):
            sum_of_products += int(number_to_update[j])*int(number_weight_factors[j])
        remainder_of_sum = sum_of_products % 11
        remaining_number = 11 - remainder_of_sum
        if(remaining_number == 10):
            check_digit = 0
        elif(remaining_number == 11):
            check_digit = 5
        else:
            check_digit = remaining_number
        article_number = prefix_code + number_to_update + str(check_digit) + postfix_code
        number_to_update_integer = int(number_to_update)
        number_to_update_integer = number_to_update_integer + 1
        number_to_update = str(number_to_update_integer)
        _logger.info("Generated article number is : %s and the number updated in the database is : %s", article_number, number_to_update)
        if SERVICE == "BP":
            company.sudo().write({'barcode_series_bp': number_to_update})
        elif SERVICE == "SP":
            company.sudo().write({'barcode_series_sp': number_to_update})
        return article_number

    # def outboundTracking(self):
    #     try:
    #         data = {"Cust_Id": os.getenv('CUSTOMER_ID'),"Event_Code":"LE","Event_Date":"02082024"}
    #         url = os.getenv('INDIA_POST_OUTBOUND_API_URL')
    #         headers = {
    #                 'Content-Type': 'application/json',
    #         }
    #         try:
    #             response = requests.post(url, headers=headers, json=data)
    #             response.raise_for_status()
    #             json_response = response.json()
    #             _logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Success %s", json_response)
    #             return json.dumps({"success": True, "payload": json_response})
    #         except requests.exceptions.RequestException as e:
    #             _logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E1 %s", str(e))
    #             return json.dumps({"success": False, "error": str(e)})
    #     except Exception as e:
    #         _logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E2 %s", str(e))
    #         return json.dumps({"success": False, "error": str(e)})