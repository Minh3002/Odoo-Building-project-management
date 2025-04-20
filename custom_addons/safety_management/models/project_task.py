from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    safety_description = fields.Text(string="Mô tả vấn đề an toàn")
    safety_measures = fields.Text(string="Biện pháp an toàn")

    safety_attachment = fields.Binary(string="Tài liệu an toàn")
    safety_attachment_name = fields.Char(string="Tên tài liệu")

    safety_image = fields.Binary(string="Hình ảnh minh họa")
    
