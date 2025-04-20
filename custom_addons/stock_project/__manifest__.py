{
    'name': 'Stock Project Integration',
    'version': '1.0',
    'summary': 'Liên kết kho với dự án',
    'author': 'manh le',
    'depends': ['base','stock', 'project'],  # Kế thừa module Stock & Project
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
}
