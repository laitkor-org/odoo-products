{
    'name': "URL Slug Optimizer",
    'summary': "Redirect SEO-friendly URLs to the original URLs with this module",
    'description': """
Odoo Controller - Working Explanation
=====================================
This Odoo controller handles custom HTTP requests, allowing data to be retrieved and processed
from the Odoo backend. It provides endpoints for fetching records and interacting with Odoo models.
Features
--------
- Handles incoming HTTP requests and routes them to the correct functions.
- Retrieves data from specific Odoo models.
- Processes input parameters and returns structured JSON responses.
- Includes error handling for invalid requests.
Working
-------
1. When a request is made to the specified route, the controller extracts any parameters.
2. It fetches relevant records from the Odoo database using the ORM.
3. The fetched data is converted into a JSON-compatible format.
4. A response is returned to the client, providing the requested information or an error message.
Possible Enhancements
---------------------
- Implement authentication for secured endpoints.
- Add more error-handling mechanisms to manage invalid data.
- Optimize database queries to improve performance.
    """,
    'price': 48,
    'currency': 'USD',
    'author': "Laitkor Consultancy Services Pvt. Ltd.",
    'maintainer': "Laitkor Consultancy Services Pvt. Ltd.",
    'category': 'Website',
    'version': '17.0',
    'depends': ['base', 'website', 'product', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/seo_friendly_url_views.xml',
    ],
    'license': 'LGPL-3',  # Fixed 'licence' to 'license'
    'images': ['static/description/banner.jpg'],  # Added cover image (thumbnail)
    'icon': 'static/description/icon.jpg',  # Added icon
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}