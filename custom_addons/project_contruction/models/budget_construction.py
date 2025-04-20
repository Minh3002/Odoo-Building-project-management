from odoo import models, fields, api

class BudgetConstruction(models.Model):
    _name = 'budget.construction'
    _description = 'Ngân sách dự án'

    
    name = fields.Char(string="Tên chi tiêu", required=True)
    description = fields.Text(string='Mô tả chi tiết')
    project_id = fields.Many2one('project.construction', string="Dự án", ondelete='cascade', required=True)
    task_id = fields.Many2one('task.construction', string="Hạng mục", ondelete='cascade' )
    upload_date = fields.Datetime(string="Ngày tải lên", default=fields.Datetime.now)

    spent_amount = fields.Float(string="Số tiền", required=True)

    attachment_ids = fields.Binary(string="Tệp đính kèm")

    amount_type = fields.Selection([
        ('fixed costs', 'Chi phí cố định'),
        ('costs incurred', 'Chi phí phát sinh'),
        ('additional budget', 'Cấp thêm chi phí'),
    ], string="Loại chi tiêu", default='fixed costs', required=True)

    created_by = fields.Many2one('res.users', string="Người tạo", default=lambda self: self.env.user, required=True)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            task_id = vals.get("task_id")
            if task_id:
                task = self.env["task.construction"].browse(task_id)
                if task and task.project_id:
                    vals["project_id"] = task.project_id.id  # Gán project từ task

        return super(BudgetConstruction, self).create(vals_list)