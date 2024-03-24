{
    'name': 'Vendor Bank Charges',
    'version': '17.0.1.0.1',
    'category': 'Accounting',
    'summary': """Payment Bank Charges""",
    'author': 'Anzal',
    'company': '',
    'maintainer': '',
    'depends': ['base', 'account','base_accounting_kit'],
    'data': [
        'views/view.xml',
        'views/payment_view.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}