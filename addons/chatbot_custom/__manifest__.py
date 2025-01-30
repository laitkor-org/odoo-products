{
    'name': 'chatbot_custom',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Custom Chatbot for Website',
    'author': 'Laitkor Consultancy Services',
    'depends': ['website'],
    'data': [
        'views/chatbot_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/chatbot_custom/static/src/js/chatbot.js',
            '/chatbot_custom/static/src/css/chatbot.css',
        ],
    },
    'installable': True,
    'application': False,
}
