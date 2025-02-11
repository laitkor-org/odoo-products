# -*- coding: utf-8 -*-
{
    'name': "URL Slug Optimizer",
    'summary': "Redirect SEO friendly URLs to the original URLs with this module",
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
    'price': 1.99,
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
    'licence': 'LGPL-3',
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
# {
#     'name': "URL Slug Optimizer",
#     'summary': "Redirect SEO-friendly URLs to the original URLs with this module",
#     'description': """
#         <div>
#             <h2>Odoo Controller - Working Explanation</h2>
#             <p>This Odoo controller handles custom HTTP requests, allowing data to be retrieved and processed
#             from the Odoo backend. It provides endpoints for fetching records and interacting with Odoo models.</p>

#             <h3>Features</h3>
#             <ul>
#                 <li>Handles incoming HTTP requests and routes them to the correct functions.</li>
#                 <li>Retrieves data from specific Odoo models.</li>
#                 <li>Processes input parameters and returns structured JSON responses.</li>
#                 <li>Includes error handling for invalid requests.</li>
#             </ul>

#             <h3>Working</h3>
#             <p>
#                 1. When a request is made to the specified route, the controller extracts any parameters.<br>
#                 2. It fetches relevant records from the Odoo database using the ORM.<br>
#                 3. The fetched data is converted into a JSON-compatible format.<br>
#                 4. A response is returned to the client, providing the requested information or an error message.
#             </p>

#             <h3>Possible Enhancements</h3>
#             <ul>
#                 <li>Implement authentication for secured endpoints.</li>
#                 <li>Add more error-handling mechanisms to manage invalid data.</li>
#                 <li>Optimize database queries to improve performance.</li>
#             </ul>
#         </div>
#     """,
#     'price': 1.99,
#     'currency': 'USD',
#     'author': "Laitkor Consultancy Services Pvt. Ltd.",
#     'maintainer': "Laitkor Consultancy Services Pvt. Ltd.",
#     'category': 'Website',
#     'version': '17.0',
#     'depends': ['base', 'website', 'product', 'web'],
#     'data': [
#         'security/ir.model.access.csv',
#         'views/seo_friendly_url_views.xml',
#     ],
#     'license': 'LGPL-3',  # Fixed 'licence' to 'license'
#     'images': ['static/slug-optimize-banner.jpg'],  # Added cover image (thumbnail)
#     'icon': 'static/url-slug-optimizer-icon.jpg',  # Added icon
#     'demo': [],
#     'qweb': [],
#     'installable': True,
#     'application': True,
#     'auto_install': False,
# }
