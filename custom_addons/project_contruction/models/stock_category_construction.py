
from odoo import models, fields

class StockCategoryConstruction(models.Model):
    _name = 'stock.category.construction'
    _description = 'Danh mục vật tư'

    name = fields.Char(string="Tên danh mục", required=True)
