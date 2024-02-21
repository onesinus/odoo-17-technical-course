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
        # 'data/templates/example_email_template.xml',

        # views
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_tag.xml',
        'views/users.xml',
        'views/menu.xml', # the order position matter!

        # Load demo data
        'demo/estate.property.tag.xml',

        # Load initial Data
        'data/estate.property.csv',
        'data/res.groups.csv',
        'data/ir.model.access.csv',

        # Schedulers
        'views/schedulers/estate_property_scheduler.xml',

        # Reports
        'views/reports/output_pdf/estate_property.xml',
    ]
}