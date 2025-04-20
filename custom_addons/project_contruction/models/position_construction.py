from odoo import models, fields

class PositionConstruction(models.Model):
    _name = 'position.construction'
    _description = 'Construction Position'

    name = fields.Char(string='Tên vị trí', required=True, tracking=True)


