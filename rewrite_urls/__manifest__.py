# -*- coding: utf-8 -*-
{
    'name': "URL Slug Optimizer",
    'summary': "Redirect SEO friendly URLs to the original URLs with this module",
    'description': """
    <h1>Odoo Controller - Working Explanation</h1>
    <p>
        This Odoo controller handles custom HTTP requests, allowing data to be retrieved and processed
        from the Odoo backend. It provides endpoints for fetching records and interacting with Odoo models.
    </p>
    <h2>Features</h2>
    <ul>
        <li>Handles incoming HTTP requests and routes them to the correct functions.</li>
        <li>Retrieves data from specific Odoo models.</li>
        <li>Processes input parameters and returns structured JSON responses.</li>
        <li>Includes error handling for invalid requests.</li>
    </ul>
    <h2>Working</h2>
    <p>
        1. When a request is made to the specified route, the controller extracts any parameters.<br>
        2. It fetches relevant records from the Odoo database using the ORM.<br>
        3. The fetched data is converted into a JSON-compatible format.<br>
        4. A response is returned to the client, providing the requested information or an error message.
    </p>
    <h2>Possible Enhancements</h2>
    <ul>
        <li>Implement authentication for secured endpoints.</li>
        <li>Add more error-handling mechanisms to manage invalid data.</li>
        <li>Optimize database queries to improve performance.</li>
    </ul>
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

