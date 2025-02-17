{
    'name': "URL Slug Optimizer",
    'summary': "Redirect SEO-friendly URLs to the original URLs with this module",
    'description': "Redirect SEO-friendly URLs to the original URLs with this module",
    'price': 48,
    'currency': 'USD',
    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'maintainer': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Website',
    'version': '17.0',
    'depends': ['base', 'website', 'product', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/seo_friendly_url_views.xml',
    ],
    'license': 'LGPL-3',  # Fixed 'licence' to 'license'
    'images': ['static/description/banner.jpg'],  # Added cover image (thumbnail)
    'icon': 'static/description/icon.jpg',  # Added icon
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}