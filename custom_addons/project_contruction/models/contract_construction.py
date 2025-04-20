import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ContractConstruction(models.Model):
    _name = 'contract.construction'
    _description = 'Contract Construction'

    name = fields.Char(string='Tên hợp đồng', required=True, help='Công ty ABC')
    contract_description = fields.Text(string="Mô tả nội dung hợp đồng")
    member_a = fields.Char(string='Bên A', required=True,)
    member_b = fields.Char(string='Bên B', required=True,)
    first_member_id = fields.Many2one('member.construction', string='Bên A: ', ondelete='cascade')
    second_member_id = fields.Many2one('member.construction', string='Bên B: ', ondelete='cascade')

    contract_attachment = fields.Binary(string="Tệp đính kèm", required=True)
    start_date = fields.Date(string='Ngày bắt đầu', required=True)
    end_date = fields.Date(string='Ngày hết hạn', required=True)
    project_id = fields.Many2one('project.construction', string='Project', ondelete='cascade' )
    task_id = fields.Many2one('task.construction', string='Hạng mục', ondelete='cascade' )

    status = fields.Selection([
        ('draft', 'Nháp'),
        ('ongoing', 'Có hiệu lực'),
        ('completed', 'Hết hiệu lực')
    ], string='Status', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            task_id = vals.get("task_id")
            if task_id:
                task = self.env["task.construction"].browse(task_id)
                if task and task.project_id:
                    vals["project_id"] = task.project_id.id  # Gán project từ task

        return super(ContractConstruction, self).create(vals_list)
