from odoo import models, fields, api

class DocumentConstruction(models.Model):
    _name = 'document.construction'
    _description = 'Construction Document'

    document_name = fields.Text(string="Tên tài liệu")
    document_description = fields.Text(string="Mô tả tài liệu")
    upload_date = fields.Datetime(string="Ngày tải lên", default=fields.Datetime.now)
    document_attachment = fields.Binary(string="Tệp đính kèm")
    document_attachment_name = fields.Char(string="Tên tệp")

    project_id = fields.Many2one('project.construction', string='Project', ondelete='cascade' )
    task_id = fields.Many2one('task.construction', string='Hạng mục', ondelete='cascade' )
    created_by = fields.Many2one('res.users', string="Người tạo", default=lambda self: self.env.user, required=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            task_id = vals.get("task_id")
            if task_id:
                task = self.env["task.construction"].browse(task_id)
                if task and task.project_id:
                    vals["project_id"] = task.project_id.id  # Gán project từ task

        return super(DocumentConstruction, self).create(vals_list)