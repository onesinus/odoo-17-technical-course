# -*- coding: utf-8 -*-
{
    'name': "Auto Backup Database To Google Cloud Storage (GCS)",

    'summary': """
        Backup Your Odoo Apps using Google Cloud Storage (GCS)""",

    'description': """
        This module helps you to make auto backup for your database odoo to Google Cloud Storage (GCS).
        Using a credential file (.json) format.
        
        Backup file options: .sql & .zip
        
     Prerequisites:
            1. google-cloud-storage python package
               Well Tested Version: google-cloud-storage==2.9.0

            2. At least one VALID Backup To GCP Configuration
               (You can setup it in this menu Settings > Backup > Google Cloud Configuration)

            3. At least one VALID Outgoing Mail Servers record
               (if you want to activate email notification)
    """,

    'author': "Codesev",
    'website': "https://codesev.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/config_view.xml',
    ],
    'currency': 'usd',
    'price': 0,
    'license': 'OPL-1',
    'images': [
        'static/description/icon.png',
    ],
    'application': True,
    'installable': True,
}
