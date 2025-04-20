{
    'name': 'Project Safety Management',
    'version': '1.0',
    'summary': 'Quản lý an toàn lao động trong dự án Odoo',
    'author': 'manh le',
    'depends': ['base','project'],  # Kế thừa module Project
    'data': [
        'security/ir.model.access.csv',  # Phân quyền
        'views/project_views.xml',  # Giao diện
    ],
    'installable': True,
    'application': False,
}
