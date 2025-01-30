# -*- coding: utf-8 -*-
{
    'name': "Update Email Template",

    'summary': "Change email templates by overriding them",

    'description': """
This module allows you to make changes to the already existing email templates
    """,

    'author': "Laitkor Consultancy Services Pvt. Ltd.",

    'category': 'Email',
    'version': '0.1',

    'depends': ['base', 'mail', 'account'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/order_confirmation_email_template.xml',
        'views/invoice_email_template.xml',
        'views/gift_card_email_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

