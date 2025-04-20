from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    document_name = fields.Text(string="Tên tài liệu")
    document_description = fields.Text(string="Mô tả tài liệu")
    upload_date = fields.Datetime(string="Ngày tải lên", default=fields.Datetime.now)
    document_attachment = fields.Binary(string="Tệp đính kèm")
    document_attachment_name = fields.Char(string="Tên tệp")

    
