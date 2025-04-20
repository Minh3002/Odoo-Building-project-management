from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    stock_picking_ids = fields.One2many('stock.picking', 'project_id', string="Danh sách Vật liệu")
