{
    'name': 'Verified Product Reviews',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Allow only customers who purchased a product to leave reviews',
    'author': 'Your Name',
    'depends': ['website', 'website_sale', 'rating'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
}
