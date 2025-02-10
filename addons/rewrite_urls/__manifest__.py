# -*- coding: utf-8 -*-
{
    'name': "rewrite_urls",
    'version': '1.0',    
    'summary': "Redirect SEO friendly URLs to the original URLs with this module",
    'description': """
This module allows us to map SEO friendly URLs with the original URLs.
    """,
    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Website',
    'depends': ['base', 'website', 'product', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/seo_friendly_url_views.xml',
    ],
    'installable':True,
    'application':True,
    'auto_install':False
}

