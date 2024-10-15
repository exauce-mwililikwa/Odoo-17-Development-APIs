# -*- coding: utf-8 -*-
{
    'name': "API",
    'module_type': 'community',
    'summary': "API",
    'description': """
       API
    """,

    'author': "Exauce mwililikwa",
    'website': "https://www.virunga.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.0.12.2',

    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        # Ajoute le fichier de sécurité ici
    ],

    # always loaded

    # only loaded in demonstration mode

    'application': True,
    'installable': True,

}
