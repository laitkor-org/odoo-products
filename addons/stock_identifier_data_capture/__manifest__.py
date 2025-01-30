{
    'name': 'ScanStock',
    'version': '1.0',
    'summary': 'Module to generate barcodes and QR codes for stock identifiers',
    'depends': ['base', 'account', 'product', 'sale'],
    'data': [
        'views/stock_identifier_views.xml',
        'views/shipping_label_wizard_views.xml',
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        # 'data/server_actions.xml',
        'security/ir.model.access.csv',
        'report/report_action.xml',
    ],
    'installable': True,
    'application': False,
}
