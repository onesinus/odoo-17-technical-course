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
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/estate_property.xml',
    ]
}