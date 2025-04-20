from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

class StockMaterial(models.Model):
    _name = 'stock.construction'
    _description = 'Quản lý vật tư và thiết bị'

    name = fields.Char(string="Tên vật tư/thiết bị", required=True)
    description = fields.Text(string='Mô tả')
    category_id = fields.Many2one('stock.category.construction', string="Danh mục")
    quantity = fields.Integer(string="Số lượng dự tính", default=1)
    actual_quantity = fields.Integer(string="Số lượng thực tế", default=1)
    amount = fields.Float(string="Giá tiền 1 vật tư (ban đầu)", default= 0)
    actual_amount = fields.Float(string="Giá tiền 1 vật tư (thực tế)", defaulactual_t= 0)

    suplier_name = fields.Text(string='Tên nhà cung cấp')
    phone = fields.Char(string='Số điện thoại')

    project_id = fields.Many2one('project.construction', string="Dự án liên quan")
    task_id = fields.Many2one('task.construction', string='Hạng mục', ondelete='cascade' )

    @api.constrains('phone')
    def _check_phone_format(self):
        phone_regex = re.compile(r'^\+?\d{10,15}$')  # Hỗ trợ số điện thoại 10-15 số
        for record in self:
            if record.phone and not phone_regex.match(record.phone):
                raise ValidationError("Số điện thoại không hợp lệ! Vui lòng nhập đúng định dạng.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            task_id = vals.get("task_id")
            if task_id:
                task = self.env["task.construction"].browse(task_id)
                if task and task.project_id:
                    vals["project_id"] = task.project_id.id  # Gán project từ task

        return super(StockMaterial, self).create(vals_list)