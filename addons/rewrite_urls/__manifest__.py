# -*- coding: utf-8 -*-
{
    'name': "rewrite_urls",

    'summary': "Redirect SEO friendly URLs to the original URLs with this module",

    'description': """
This module allows us to map SEO friendly URLs with the original URLs.
    """,

    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Website',
    'version': '1.0',

    'depends': ['base', 'website', 'product', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/seo_friendly_url_views.xml',
    ],
}

