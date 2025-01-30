# -*- coding: utf-8 -*-
{
    'name': "Delivery - Custom",

    'summary': "Let's call the APIs required for delivery",

    'description': """
This module allow you to integrate with a delivery partner such as India Post.
    """,

    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Inventory/Delivery',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/delivery_tracking_confirmation.xml',
        'views/sale_order_views.xml',
        'report/shipping_label_lucknow_reports.xml',
        'report/shipping_label_lucknow_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'delivery_post/static/src/css/order_tracking_page.css',
            'delivery_post/static/src/js/delivery_post.js',
        ],
    },
}

