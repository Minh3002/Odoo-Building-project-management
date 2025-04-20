from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    risk_level = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
    ], string="Mức độ rủi ro", default='low')

    risk_description = fields.Text(string="Mô tả rủi ro")
    risk_mitigation = fields.Text(string="Biện pháp giảm thiểu")
