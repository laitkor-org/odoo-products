from odoo import http
from odoo.http import request
import logging
from odoo.addons.website.controllers.main import Website
from markupsafe import Markup

_logger = logging.getLogger(__name__)

class WebsiteProductVariantSearch(Website):

    @http.route('/website/snippet/autocomplete', type='json', auth='public', website=True)
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        """
        Extend the default autocomplete method to include product variants in search results.
        """
        original_results = super(WebsiteProductVariantSearch, self).autocomplete(
            search_type=search_type,
            term=term,
            order=order,
            limit=limit,
            max_nb_chars=max_nb_chars,
            options=options
        )

        if not term:
            return original_results

        variant_domain = [
            ('product_template_attribute_value_ids.name', 'ilike', term),
        ]
        variants = request.env['product.product'].sudo().search(variant_domain, limit=limit)
        additional_results = []
        for variant in variants:
            product = variant.product_tmpl_id
            categories = product.public_categ_ids
            category_buttons = request.env['ir.ui.view']._render_template(
                "website_sale.product_category_extra_link",
                {'categories': categories}
                )
            additional_results.append({
                '_fa': 'fa-shopping-cart',
                'name': product.name,
                'website_url': Markup(f'{variant.website_url}'),
                'image_url': Markup(f'/web/image/product.template/{product.id}/image_128'),
                'description': product.description or '',
                # 'detail': Markup(f"{request.website.currency_id.symbol}<span class='oe_currency_value'>{product.list_price:.2f}</span>"),
                'price': f"{request.website.currency_id.symbol} {product.list_price}",
                'category': ', '.join(product.public_categ_ids.mapped('name')) if product.public_categ_ids else None,
                # 'extra_link': Markup(category_buttons) if categories else '',
                'detail_strike': '',
                'is_variant': True,
                'variant_sku': variant.default_code or 'No SKU', 
                'variant_name': ', '.join(variant.product_template_attribute_value_ids.mapped('name')) or 'No attributes',
            })

        original_results['results'].extend(additional_results)

        _logger.info(f"Autocomplete enhanced results: {original_results}")
        return original_results
