{
    'name': 'Document Management',
    'version': '1.0',
    'summary': 'Quản lý tài liệu theo công việc',
    'author': 'manh le',
    'depends': ['base','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
}
