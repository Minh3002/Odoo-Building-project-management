{
    'name': 'Task Construction',
    'version': '0.1',
    'category': 'Construction',
    'summary': 'Manage task of construction project',
    'description': 'Manage construction tasks with subtasks and members',
    'author': 'manh le',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_construction_views.xml',
    ],
    'installable': True,
    'application': True,
}