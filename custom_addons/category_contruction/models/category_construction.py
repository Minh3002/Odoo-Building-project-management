
from odoo import models, fields

class CategoryConstruction(models.Model):
    _name = 'category.construction'
    _description = 'category Construction'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
