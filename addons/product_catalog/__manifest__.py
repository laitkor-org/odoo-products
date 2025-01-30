# -*- coding: utf-8 -*-
{
    'name': 'Product Catalog Generator',
    'version': '1.0',
    'summary': 'Generates a simple product catalog',
    'description': 'Module to generate a basic product catalog.',
    'category': 'Tools',
    'author': 'Laitkor Consultancy Services',
    'images': ['static/description/icon.png'],
    'website': 'https://laitkor.com',
    'depends': ['base', 'product'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
