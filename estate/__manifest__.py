{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Onesinus Tamba",
    'category': 'App',
    'description': """
        This module is used to learn basic odoo 17 technical
    """,
    'application': True,
    'data': [


        # Security
        'security/ir.model.access.csv',

        # templates
        'data/templates/example_email_template.xml',

        # views
        'views/menu.xml',
        'views/estate_property.xml',

        # Load initial Data
        'data/estate.property.csv',

        # Schedulers
        'views/schedulers/estate_property_scheduler.xml'        
    ]
}