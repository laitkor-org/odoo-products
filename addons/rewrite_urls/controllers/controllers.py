# from odoo import http
# from odoo.http import request
# from werkzeug.utils import redirect
# from werkzeug.exceptions import NotFound
# import logging
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# import re

# class CustomWebsiteSale(WebsiteSale):

#     @http.route([
#     '/<path:seo_friendly_url>',
#     '/shop/<path:seo_friendly_url>',
#     '/shop/category/<path:seo_friendly_url>'
#     ], auth='public', website=True)
#     def handle_seo_urls(self, seo_friendly_url, **kwargs):
#         logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")
#         request_path = request.httprequest.path

#         search_condition = seo_friendly_url
#         if request_path.startswith('/shop/category/'):
#             logging.info("Inside IF")
#             search_condition = f"/shop/category/{seo_friendly_url}"
#         elif request_path.startswith('/shop/'):
#             search_condition = f"/shop/{seo_friendly_url}"
#         else:
#             search_condition = f"/{seo_friendly_url}"
#         seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#             ('seo_friendly_url', '=', search_condition)
#         ], limit=1)

#         if seo_url:
#             return request.redirect(seo_url.original_url)

#         return request.not_found()
    

# class CustomWebsiteSale(WebsiteSale):

#     @http.route('/<path:seo_friendly_url>', auth='public', website=True)
#     def find_template(self, seo_friendly_url, **kwargs):
#         URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#             ('seo_friendly_url', 'ilike', f"/{seo_friendly_url}")
#         ], limit=1)
#         if(URLrecord):
#             page = request.env['website.page'].search([('url', '=', URLrecord.original_url)], limit=1)
#         else:
#             page = request.env['website.page'].search([('url', '=', f'/{seo_friendly_url}')], limit=1)
#         if page:
#             view = page.view_id
#             if view:
#                 return request.render(view.xml_id or view.id, qcontext=kwargs)
#             else:
#                 logging.info("No view found for the template.")
#         else:
#             # return request.not_found()
#             return request.render("http_routing.404")
        
#     @http.route('/shop/<string:seo_friendly_url>', auth='public', website=True)
#     def handle_product_urls(self, seo_friendly_url, **kwargs):
#         try:
#             URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#                 ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
#             ], limit=1)
#             if(URLrecord):
#                 url = URLrecord.original_url
#             else:
#                 url = f'/shop/{seo_friendly_url}'
#             try:
#                 parts = url.split('-')
#                 productId = int(re.split(r'[?#]', parts[-1])[0])
#             except (ValueError, IndexError) as e:
#                 productId = None
#             if productId:
#                 product = request.env['product.template'].sudo().search([('id', '=', productId)], limit=1)
#                 logging.info("Product ID is %s and URL is : %s", productId, seo_friendly_url)
#                 category = kwargs.get('category')
#                 search = kwargs.get('search')
#                 if category:
#                     kwargs.pop('category', None)
#                 if search:
#                     kwargs.pop('search', None)
#                 if product and category and search:
#                     return request.render("website_sale.product", self._prepare_product_values(product, str(category), str(search), **kwargs))
#                 elif product and category:
#                     return request.render("website_sale.product", self._prepare_product_values(product, str(category), '', **kwargs))
#                 elif product and search:
#                     return request.render("website_sale.product", self._prepare_product_values(product, '', str(search), **kwargs))
#                 elif product:
#                     return request.render("website_sale.product", self._prepare_product_values(product, '', '', **kwargs))
#             else:
#                 page = request.env['website.page'].search([('url', '=', url)], limit=1)
#                 if page:
#                     view = page.view_id
#                     if view:
#                         return request.render(view.xml_id or view.id, qcontext=kwargs)
#                 # return request.not_found()
#                 return request.render("http_routing.404")
#         except Exception as e:
#             logging.info("Exception being raised in the /shop endpoint %s", e)
#             # return request.not_found()
#             return request.render("http_routing.404")

##########################################################################################
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re

_logger = logging.getLogger(__name__)

class CustomWebsiteSale(WebsiteSale):

    @http.route([
        '/<path:seo_friendly_url>',
        '/shop/<path:seo_friendly_url>',
        '/shop/category/<path:seo_friendly_url>'
    ], auth='public', website=True)
    def handle_seo_urls(self, seo_friendly_url, **kwargs):
        _logger.info(f"Received SEO-friendly URL: {seo_friendly_url}")
        request_path = request.httprequest.path
        _logger.info(f"Request Path: {request_path}")

        search_condition = seo_friendly_url
        if request_path.startswith('/shop/category/'):
            search_condition = f"/shop/category/{seo_friendly_url}"
        elif request_path.startswith('/shop/'):
            search_condition = f"/shop/{seo_friendly_url}"
        else:
            search_condition = f"/{seo_friendly_url}"
        
        _logger.info(f"Searching for SEO-friendly URL in database: {search_condition}")

        seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
            ('seo_friendly_url', '=', search_condition)
        ], limit=1)

        if seo_url:
            _logger.info(f"Found matching SEO URL: {seo_url.original_url}, Fetch Content: {seo_url.fetch_content}")

            if seo_url.fetch_content:
                _logger.info(f"Fetch content is TRUE. Rendering content for: {seo_friendly_url}")
                return self.find_template(seo_friendly_url, **kwargs)
            else:
                _logger.info(f"Fetch content is FALSE. Redirecting to: {seo_url.original_url}")
                return request.redirect(seo_url.original_url)

        _logger.warning(f"No matching SEO URL found for: {seo_friendly_url}. Returning 404.")
        return request.not_found()


    def find_template(self, seo_friendly_url, **kwargs):
        """Handles rendering pages when fetch_content is True"""
        _logger.info(f"Attempting to render page for SEO-friendly URL: {seo_friendly_url}")

        request_path = request.httprequest.path
        is_shop_page = request_path.startswith('/shop')

        if is_shop_page:
            _logger.info("Detected `/shop` URL. Searching for categories and products.")

            # Search for a matching URL record
            URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
                ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
            ], limit=1)

            url = URLrecord.original_url if URLrecord else f'/shop/{seo_friendly_url}'

            try:
                parts = url.split('-')
                productId = int(re.split(r'[?#]', parts[-1])[0])
            except (ValueError, IndexError) as e:
                _logger.warning(f"Failed to extract product ID from URL: {url}. Error: {e}")
                productId = None

            if productId:
                product = request.env['product.template'].sudo().search([('id', '=', productId)], limit=1)
                _logger.info(f"Product ID: {productId}, Product Name: {product.name if product else 'Not Found'}")

                category = kwargs.pop('category', None)
                search = kwargs.pop('search', None)

                _logger.info(f"Rendering product page with Category: {category}, Search: {search}")

                if product:
                    return request.render("website_sale.product", self._prepare_product_values(product, category or '', search or '', **kwargs))

            _logger.info(f"No product found for {seo_friendly_url}. Checking for website pages.")

            # If no product is found, check for a website page
            page = request.env['website.page'].sudo().search([('url', '=', url)], limit=1)
            if page and page.view_id:
                _logger.info(f"Page found: {page.name}, Rendering view: {page.view_id.xml_id or page.view_id.id}")
                return request.render(page.view_id.xml_id or page.view_id.id, qcontext=kwargs)

        _logger.warning(f"No matching product or page found for {seo_friendly_url}. Returning 404.")
        return request.render("http_routing.404")



