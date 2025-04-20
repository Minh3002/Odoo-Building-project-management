from odoo import models, fields

class ProjectSafety(models.Model):
    _inherit = 'project.project'

    safety_ids = fields.One2many('project.safety', 'project_id', string="Vấn đề An toàn")
    
    _name = 'project.safety'
    _description = 'An toàn Lao động trong Dự án'
    
    project_id = fields.Many2one('project.project', string="Dự án", required=True, ondelete='cascade')
    issue = fields.Text(string="Vấn đề An toàn", required=True)
    solution = fields.Text(string="Giải pháp An toàn")
    status = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('resolved', 'Đã xử lý'),
    ], string="Trạng thái", default='pending')
    
    assigned_to = fields.Many2one('res.users', string="Người chịu trách nhiệm")
    date_reported = fields.Date(string="Ngày báo cáo", default=fields.Date.context_today)
