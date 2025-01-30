from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re

# class RewriteUrls(http.Controller):
# class CustomWebsiteSale(WebsiteSale):
    # old code
    # @http.route('/<path:seo_friendly_url>', auth='public', website=True)
    # def find_template(self, seo_friendly_url, **kwargs):
    #     URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #         ('seo_friendly_url', 'ilike', f"/{seo_friendly_url}")
    #     ], limit=1)
    #     if(URLrecord):
    #         page = request.env['website.page'].search([('url', '=', URLrecord.original_url)], limit=1)
    #     else:
    #         page = request.env['website.page'].search([('url', '=', f'/{seo_friendly_url}')], limit=1)
    #     if page:
    #         view = page.view_id
    #         if view:
    #             return request.render(view.xml_id or view.id, qcontext=kwargs)
    #         else:
    #             logging.info("No view found for the template.")
    #     else:
    #         # return request.not_found()
    #         return request.render("http_routing.404")
        
    # @http.route('/shop/<string:seo_friendly_url>', auth='public', website=True)
    # def handle_product_urls(self, seo_friendly_url, **kwargs):
    #     try:
    #         URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #             ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
    #         ], limit=1)
    #         if(URLrecord):
    #             url = URLrecord.original_url
    #         else:
    #             url = f'/shop/{seo_friendly_url}'
    #         try:
    #             parts = url.split('-')
    #             productId = int(re.split(r'[?#]', parts[-1])[0])
    #         except (ValueError, IndexError) as e:
    #             productId = None
    #         if productId:
    #             product = request.env['product.template'].sudo().search([('id', '=', productId)], limit=1)
    #             logging.info("Product ID is %s and URL is : %s", productId, seo_friendly_url)
    #             category = kwargs.get('category')
    #             search = kwargs.get('search')
    #             if category:
    #                 kwargs.pop('category', None)
    #             if search:
    #                 kwargs.pop('search', None)
    #             if product and category and search:
    #                 return request.render("website_sale.product", self._prepare_product_values(product, str(category), str(search), **kwargs))
    #             elif product and category:
    #                 return request.render("website_sale.product", self._prepare_product_values(product, str(category), '', **kwargs))
    #             elif product and search:
    #                 return request.render("website_sale.product", self._prepare_product_values(product, '', str(search), **kwargs))
    #             elif product:
    #                 return request.render("website_sale.product", self._prepare_product_values(product, '', '', **kwargs))
    #         else:
    #             page = request.env['website.page'].search([('url', '=', url)], limit=1)
    #             if page:
    #                 view = page.view_id
    #                 if view:
    #                     return request.render(view.xml_id or view.id, qcontext=kwargs)
    #             # return request.not_found()
    #             return request.render("http_routing.404")
    #     except Exception as e:
    #         logging.info("Exception being raised in the /shop endpoint %s", e)
    #         # return request.not_found()
    #         return request.render("http_routing.404")




    # code that might be required for future for redirection (301)
    # @http.route('/<path:seo_friendly_url>', auth='public', website=True)
    # def handle_seo_url(self, seo_friendly_url, **kwargs):
    #     logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")

    #     seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #         ('seo_friendly_url', '=', seo_friendly_url)
    #     ], limit=1)
    #     if seo_url:
    #         return request.redirect(seo_url.original_url)

    # @http.route('/shop/<string:seo_friendly_url>', auth='public', website=True)
    # def handle_seo_url(self, seo_friendly_url, **kwargs):
        
    #     logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")
    #     seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #         ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
    #     ], limit=1)
    #     if seo_url:
    #         return request.redirect(seo_url.original_url)
    #     return None
        
    # @http.route('/shop/category/<string:category_name>', auth='public', website=True)
    # def handle_category_url(self, category_name, **kwargs):
     
    #     logging.info(f"Received SEO-friendly URL: {category_name}")
    #     category = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #         ('seo_friendly_url', 'ilike', f"/shop/category/{category_name}")
    #     ], limit=1)
    #     if category:
    #         return request.redirect(category.original_url)
    #     return None


        
    # new code
    # @http.route('/<path:seo_friendly_url>', auth='public', website=True)
    # def handle_seo_url(self, seo_friendly_url, **kwargs):
    #     logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")

    #     # Check for exact match in rewrite URLs
    #     seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #         ('seo_friendly_url', '=', f"/{seo_friendly_url}")
    #     ], limit=1)

    #     if seo_url:
    #         logging.info(f"Redirecting to original URL: {seo_url.original_url}")
    #         return request.redirect(seo_url.original_url)

    #     if seo_friendly_url.startswith('shop'):
    #         # Check if it's a category
    #         if 'category/' in seo_friendly_url:
    #             category_name = seo_friendly_url.split('category/')[1]
    #             category = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #                 ('seo_friendly_url', 'ilike', f"/shop/category/{category_name}")
    #             ], limit=1)
    #             if category:
    #                 logging.info(f"Redirecting category to: {category.original_url}")
    #                 return request.redirect(category.original_url)
    #         else:
    #             # Handle `/shop/<seo_friendly_url>`
    #             shop_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
    #                 ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
    #             ], limit=1)
    #             if shop_url:
    #                 logging.info(f"Redirecting shop URL to: {shop_url.original_url}")
    #                 return request.redirect(shop_url.original_url)

    #     # If no match, return 404
    #     logging.warning(f"No matching URL found for: {seo_friendly_url}")
    #     return request.render('http_routing.404')

    # def render_404(self):
    #     """Render a custom 404 page."""
    #     try:
    #         return request.render('website.404')  # Default 404 template for website module
    #     except Exception as e:
    #         logging.error(f"Failed to render 404 page: {str(e)}")
    #         # Fallback HTML response for 404
    #         return request.make_response("<h1>404: Page not found</h1>", status=404)

# class RewriteUrls(http.Controller):
#     @http.route('/<path:seo_friendly_url>', auth='public', website=True)
#     def handle_seo_friendly_url(self, seo_friendly_url, **kwargs):
#         """
#         Handles all SEO-friendly URLs, including `/shop`, product pages, and general pages.
#         """
#         try:
#             logging.info(f"Handling URL: {seo_friendly_url}")

#             # Check for rewrite rule
#             url_record = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#                 ('seo_friendly_url', 'ilike', f"/{seo_friendly_url}")
#             ], limit=1)

#             target_url = url_record.original_url if url_record else f'/{seo_friendly_url}'

#             # 1. Handle `/shop` URLs conditionally
#             if target_url.startswith('/shop'):
#                 return self._handle_shop_url(target_url, **kwargs)

#             # 2. Attempt to find and render a `website.page`
#             page = request.env['website.page'].sudo().search([('url', '=', target_url)], limit=1)
#             if page and page.view_id:
#                 logging.info(f"Rendering page: {page.url} (View: {page.view_id.xml_id})")
#                 return request.render(page.view_id.xml_id or page.view_id.id, qcontext=kwargs)

#             # 3. If no match, return 404
#             logging.warning(f"No matching page or shop item found for URL: {seo_friendly_url}")
#             return request.not_found()

#         except Exception as e:
#             logging.error(f"Exception while handling URL {seo_friendly_url}: {e}")
#             return request.not_found()

#     def _handle_shop_url(self, target_url, **kwargs):
#         """
#         Handles URLs under `/shop`, including product and category URLs.
#         """
#         try:
#             logging.info(f"Handling shop URL: {target_url}")

#             # Extract potential product ID from the URL
#             try:
#                 parts = target_url.split('-')
#                 product_id = int(re.split(r'[?#]', parts[-1])[0])
#             except (ValueError, IndexError):
#                 product_id = None

#             if product_id:
#                 # Fetch the product
#                 product = request.env['product.template'].sudo().search([('id', '=', product_id)], limit=1)
#                 if product:
#                     logging.info(f"Rendering product page for ID: {product_id}")
#                     category = kwargs.pop('category', None)
#                     search = kwargs.pop('search', None)
#                     return request.render(
#                         "website_sale.product",
#                         self._prepare_product_values(product, str(category or ''), str(search or ''), **kwargs)
#                     )

#             # If no product is found, attempt to render as a page
#             page = request.env['website.page'].sudo().search([('url', '=', target_url)], limit=1)
#             if page and page.view_id:
#                 logging.info(f"Rendering shop-related page: {page.url}")
#                 return request.render(page.view_id.xml_id or page.view_id.id, qcontext=kwargs)

#             return request.not_found()

#         except Exception as e:
#             logging.error(f"Error while handling shop URL: {target_url} - {e}")
#             return request.not_found()

#     def _prepare_product_values(self, product, category, search, **kwargs):
#         """
#         Prepares context values for rendering the product page.
#         """
#         return {
#             'product': product,
#             'category': category,
#             'search': search,
#             **kwargs,
#         }

class RewriteUrlsController(http.Controller):
    @http.route([
        '/<path:seo_friendly_url>',
        '/shop/<path:seo_friendly_url>',
        '/shop/category/<path:seo_friendly_url>'
    ], auth='public', website=True)
    def handle_seo_urls(self, seo_friendly_url, **kwargs):
        logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")

        # Determine the full requested path
        request_path = request.httprequest.path
        
        # Define search condition dynamically based on the request path
        search_condition = seo_friendly_url
        if request_path.startswith('/shop/category/'):
            search_condition = f"/shop/category/{seo_friendly_url}"
        elif request_path.startswith('/shop/'):
            search_condition = f"/shop/{seo_friendly_url}"

        # Search for the corresponding URL
        seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
            ('seo_friendly_url', '=', search_condition)
        ], limit=1)

        # Prevent infinite redirect loop
        # if seo_url and seo_url.original_url.strip('/') == request_path.strip('/'):
        #     logging.warning(f"Preventing self-redirect for: {request_path}")
        #     return request.not_found()

        if seo_url:
            return request.redirect(seo_url.original_url)

        return request.not_found()