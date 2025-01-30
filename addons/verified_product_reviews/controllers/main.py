   
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class RatingController(http.Controller):

    @http.route('/mail/chatter_post', type='http', auth='public', website=True)
    def review_submit(self, **kwargs):
        try:
            result = request.env['rating.rating'].create(kwargs)
            
            if isinstance(result, dict) and result.get('error'):
                return request.render('verified_product_reviews.review_denied', {
                    'error_message': result.get('message')
                })

        except Exception as e:
            _logger.error(f"Error creating a review: {str(e)}")
            return request.render('verified_product_reviews.review_denied', {
                'error_message': str(e)
            })

