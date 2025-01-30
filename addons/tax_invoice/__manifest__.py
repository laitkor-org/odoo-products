{
    'name': 'Sale Tax Invoice',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Generate a tax invoice from the sale order.',
    'description': 'Adds a button on the sale order detail page to generate a tax invoice document.',
    'author': 'Your Name',
    'depends': ['sale', 'account'],
    'data': [
        'views/sale_order_views.xml',
        'reports/sale_tax_invoice_report.xml',
        'reports/sale_tax_invoice_template.xml',
    ],
    'installable': True,
    'application': False,
}
