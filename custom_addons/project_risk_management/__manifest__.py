{
    'name': 'Project Risk Management',
    'version': '1.0',
    'summary': 'Quản lý rủi ro trong dự án Odoo',
    'author': 'manh le',
    'depends': ['base','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
}
