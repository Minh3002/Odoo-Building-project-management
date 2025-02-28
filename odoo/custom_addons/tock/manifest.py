{
    'name': 'Tock - Quản Lý Kho & Nguyên Vật Liệu',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Quản lý nguyên vật liệu và hóa đơn theo dự án xây dựng',
    'author': 'Bạn',
    'depends': ['stock', 'account', 'project'],
    'data': [
        'views/project_views.xml',
        'views/stock_views.xml',
        'views/invoice_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
}
