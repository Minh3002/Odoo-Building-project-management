from odoo import models, fields, api

class SafetyConstruction(models.Model):
    _name = 'safety.construction'
    _description = 'Construction Safety'

    name = fields.Char(string='Safety Name', required=True, tracking=True)

    safety_description = fields.Text(string="Mô tả vấn đề an toàn")
    safety_measures = fields.Text(string="Biện pháp an toàn")
    upload_date = fields.Datetime(string="Ngày tải lên", default=fields.Datetime.now)

    safety_attachment = fields.Binary(string="Tệp đính kèm")
    safety_attachment_name = fields.Char(string="Tên tài liệu")

    safety_image = fields.Binary(string="Hình ảnh minh họa")

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

        return super(SafetyConstruction, self).create(vals_list)