from odoo import models, fields

class StageConstruction(models.Model):
    _name = 'stage.construction'
    _description = 'Construction Stage Task'

    name = fields.Char(string='Tên hạng mục', required=True, tracking=True)

    sequence = fields.Integer(string='sequence stage', default=1)

    project_id = fields.Many2one('project.construction', string='Project', ondelete='cascade' )
