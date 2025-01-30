{
    'name': 'GTM Integration',
    'version': '1.0',
    'depends': ['website_sale'],
    'data': [
    ],
    'assets': {
    'web.assets_frontend': [
        'gtm_tracker/static/src/js/gtm_view_cart.js',
    ],
    },
    'installable': True,
    'application': False,
}
