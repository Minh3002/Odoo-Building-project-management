import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SubcontractorConstruction(models.Model):
    _name = 'subcontractor.construction'
    _description = 'Subcontractor Construction'

    name = fields.Char(string='Tên thầu phụ', required=True)
    contract_id = fields.Many2one('contract.construction', string='Contract', ondelete='cascade' )
    constractor_attachment = fields.Binary(string="Tệp đính kèm")
    phone = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    start_date = fields.Date(string='Ngày bắt đầu')
    end_date = fields.Date(string='Ngày hết hạn')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')

    @api.constrains('phone')
    def _check_phone_format(self):
        phone_regex = re.compile(r'^\+?\d{10,15}$')  # Hỗ trợ số điện thoại 10-15 số
        for record in self:
            if record.phone and not phone_regex.match(record.phone):
                raise ValidationError("Số điện thoại không hợp lệ! Vui lòng nhập đúng định dạng.")
    
    @api.constrains('email')
    def _check_email_format(self):
        email_regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        for record in self:
            if record.email and not email_regex.match(record.email):
                raise ValidationError("Email không hợp lệ! Vui lòng nhập đúng định dạng.")