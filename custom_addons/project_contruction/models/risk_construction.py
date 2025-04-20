from odoo import models, fields, api

class RiskConstruction(models.Model):
    _name = 'risk.construction'
    _description = 'Construction Risk'

    name = fields.Char(string='Risk Name', required=True, tracking=True)

    risk_level = fields.Selection([
        ('Low', 'Thấp'),
        ('Medium', 'Trung bình'),
        ('High', 'Cao'),
        ('Very high', 'Rất Cao'),
    ], string="Mức độ rủi ro", default='Low')

    risk_description = fields.Text(string="Mô tả rủi ro")
    risk_mitigation = fields.Text(string="Biện pháp giảm thiểu")
    upload_date = fields.Datetime(string="Ngày tải lên", default=fields.Datetime.now)

    risk_type = fields.Selection([
        ('reality', 'Thực tế'),
        ('forecast', 'Dự đoán')
    ], string="Phân loại rủi ro", default='forecast')

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

        return super(RiskConstruction, self).create(vals_list)