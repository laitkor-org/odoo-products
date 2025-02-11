# -*- coding: utf-8 -*-
{
    'name': "URL Slug Optimizer",
    'summary': "Redirect SEO friendly URLs to the original URLs with this module",
    'description': """
        This module allows us to map SEO friendly URLs with the original URLs.
    """,
    'price': 1.99,
    'currency': 'USD',
    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'maintainer': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Website',
    'version': ['17.0','18.0','16.0'],
    'depends': ['base', 'website', 'product', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/seo_friendly_url_views.xml',
    ],
    'licence': 'LGPL-3',
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

