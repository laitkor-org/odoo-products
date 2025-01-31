from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re

class CustomWebsiteSale(WebsiteSale):

    @http.route([
    '/<path:seo_friendly_url>',
    '/shop/<path:seo_friendly_url>',
    '/shop/category/<path:seo_friendly_url>'
    ], auth='public', website=True)
    def handle_seo_urls(self, seo_friendly_url, **kwargs):
        logging.info(f"Received SEO-friendly URL: {seo_friendly_url}")
        request_path = request.httprequest.path

        search_condition = seo_friendly_url
        if request_path.startswith('/shop/category/'):
            logging.info("Inside IF")
            search_condition = f"/shop/category/{seo_friendly_url}"
        elif request_path.startswith('/shop/'):
            search_condition = f"/shop/{seo_friendly_url}"
        else:
            search_condition = f"/{seo_friendly_url}"
        seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
            ('seo_friendly_url', '=', search_condition)
        ], limit=1)

        if seo_url:
            return request.redirect(seo_url.original_url)

        return request.not_found()
    

class CustomWebsiteSale(WebsiteSale):

    @http.route('/<path:seo_friendly_url>', auth='public', website=True)
    def find_template(self, seo_friendly_url, **kwargs):
        URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
            ('seo_friendly_url', 'ilike', f"/{seo_friendly_url}")
        ], limit=1)
        if(URLrecord):
            page = request.env['website.page'].search([('url', '=', URLrecord.original_url)], limit=1)
        else:
            page = request.env['website.page'].search([('url', '=', f'/{seo_friendly_url}')], limit=1)
        if page:
            view = page.view_id
            if view:
                return request.render(view.xml_id or view.id, qcontext=kwargs)
            else:
                logging.info("No view found for the template.")
        else:
            # return request.not_found()
            return request.render("http_routing.404")
        
    @http.route('/shop/<string:seo_friendly_url>', auth='public', website=True)
    def handle_product_urls(self, seo_friendly_url, **kwargs):
        try:
            URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
                ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
            ], limit=1)
            if(URLrecord):
                url = URLrecord.original_url
            else:
                url = f'/shop/{seo_friendly_url}'
            try:
                parts = url.split('-')
                productId = int(re.split(r'[?#]', parts[-1])[0])
            except (ValueError, IndexError) as e:
                productId = None
            if productId:
                product = request.env['product.template'].sudo().search([('id', '=', productId)], limit=1)
                logging.info("Product ID is %s and URL is : %s", productId, seo_friendly_url)
                category = kwargs.get('category')
                search = kwargs.get('search')
                if category:
                    kwargs.pop('category', None)
                if search:
                    kwargs.pop('search', None)
                if product and category and search:
                    return request.render("website_sale.product", self._prepare_product_values(product, str(category), str(search), **kwargs))
                elif product and category:
                    return request.render("website_sale.product", self._prepare_product_values(product, str(category), '', **kwargs))
                elif product and search:
                    return request.render("website_sale.product", self._prepare_product_values(product, '', str(search), **kwargs))
                elif product:
                    return request.render("website_sale.product", self._prepare_product_values(product, '', '', **kwargs))
            else:
                page = request.env['website.page'].search([('url', '=', url)], limit=1)
                if page:
                    view = page.view_id
                    if view:
                        return request.render(view.xml_id or view.id, qcontext=kwargs)
                # return request.not_found()
                return request.render("http_routing.404")
        except Exception as e:
            logging.info("Exception being raised in the /shop endpoint %s", e)
            # return request.not_found()
            return request.render("http_routing.404")

    


# from odoo import http
# from odoo.http import request
# from werkzeug.utils import redirect
# from werkzeug.exceptions import NotFound
# import logging
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# import re

# class RewriteUrls(http.Controller):
# # class CustomWebsiteSale(WebsiteSale):

#     @http.route('/<path:seo_friendly_url>', auth='public', website=True)
#     def find_template(self, seo_friendly_url, **kwargs):
#         URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#             ('seo_friendly_url', 'ilike', f"/{seo_friendly_url}")
#         ], limit=1)

#         if URLrecord.fetch_content:
#             if(URLrecord):
#                 page = request.env['website.page'].search([('url', '=', URLrecord.original_url)], limit=1)
#             else:
#                 page = request.env['website.page'].search([('url', '=', f'/{seo_friendly_url}')], limit=1)
#             if page:
#                 view = page.view_id
#                 if view:
#                     return request.render(view.xml_id or view.id, qcontext=kwargs)
#                 else:
#                     logging.info("No view found for the template.")
#             else:
#                 # return request.not_found()
#                 return request.render("http_routing.404")
#         else:
#             seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#                 ('seo_friendly_url', '=', seo_friendly_url)
#             ], limit=1)
#             if seo_url:
#                 return request.redirect(seo_url.original_url)
            
#     @http.route('/shop/<string:seo_friendly_url>', auth='public', website=True)
#     def handle_product_urls(self, seo_friendly_url, **kwargs):
#         try:
#             URLrecord = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#                 ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
#             ], limit=1)
#             if URLrecord.fetch_content:
#                 if(URLrecord):
#                     url = URLrecord.original_url
#                 else:
#                     url = f'/shop/{seo_friendly_url}'
#                 try:
#                     parts = url.split('-')
#                     productId = int(re.split(r'[?#]', parts[-1])[0])
#                 except (ValueError, IndexError) as e:
#                     productId = None
#                 if productId:
#                     product = request.env['product.template'].sudo().search([('id', '=', productId)], limit=1)
#                     logging.info("Product ID is %s and URL is : %s", productId, seo_friendly_url)
#                     category = kwargs.get('category')
#                     search = kwargs.get('search')
#                     if category:
#                         kwargs.pop('category', None)
#                     if search:
#                         kwargs.pop('search', None)
#                     if product and category and search:
#                         return request.render("website_sale.product", self._prepare_product_values(product, str(category), str(search), **kwargs))
#                     elif product and category:
#                         return request.render("website_sale.product", self._prepare_product_values(product, str(category), '', **kwargs))
#                     elif product and search:
#                         return request.render("website_sale.product", self._prepare_product_values(product, '', str(search), **kwargs))
#                     elif product:
#                         return request.render("website_sale.product", self._prepare_product_values(product, '', '', **kwargs))
#                 else:
#                     page = request.env['website.page'].search([('url', '=', url)], limit=1)
#                     if page:
#                         view = page.view_id
#                         if view:
#                             return request.render(view.xml_id or view.id, qcontext=kwargs)
#                     # return request.not_found()
#                     return request.render("http_routing.404")
#             else:
#                 seo_url = request.env['rewrite_urls.rewrite_urls'].sudo().search([
#                     ('seo_friendly_url', 'ilike', f"/shop/{seo_friendly_url}")
#                 ], limit=1)
#                 if seo_url:
#                     return request.redirect(seo_url.original_url)
#                 return None
                

#         except Exception as e:
#             logging.info("Exception being raised in the /shop endpoint %s", e)
#             # return request.not_found()
#             return request.render("http_routing.404")
    
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