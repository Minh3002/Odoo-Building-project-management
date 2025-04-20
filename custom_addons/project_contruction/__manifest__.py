{
    'name': 'Project Construction',
    'version': '5.4',
    'category': 'Construction',
    'summary': 'Manage construction projects',
    'description': 'Module to manage construction projects with stages, dates, and leaders.',
    'author': 'manh le',
    'depends': ['base','mail', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_construction_views.xml',
        'views/task_construction_views.xml',
        'views/stage_construction_views.xml',
        'views/risk_construction_views.xml',
        'views/safety_construction_views.xml',
        'views/document_construction_views.xml',
        'views/contract_construction_views.xml',
        'views/report_construction_views.xml',
        'views/stock_construction_views.xml',
        'views/member_construction_views.xml',
        'views/stock_category_construction_views.xml',
        'views/position_construction_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'static/src/js/task_list.js',
        ],
    },
    'installable': True,
    'application': True,
}