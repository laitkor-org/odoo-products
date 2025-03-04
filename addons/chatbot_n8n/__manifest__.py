{
    'name': 'Chatbot Integration with n8n',
    'version': '1.0',
    'summary': 'Integrate a chatbot for video consultation using n8n',
    'description': """This module integrates an n8n chatbot in Odoo for video consultations, 
    handling scheduling, user info, and payments via Razorpay.""",
    'author': 'Ujjwal Srivastava',
    'category': 'Website',
    'depends': ['website', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/chatbot_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'chatbot_n8n/static/src/js/chatbot.js',
            'chatbot_n8n/static/src/css/chatbot.css',
        ],
    },
    'assets': {},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
