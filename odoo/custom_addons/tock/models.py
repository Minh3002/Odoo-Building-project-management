from odoo import models, fields, api

class ConstructionProject(models.Model):
    _name = 'construction.project'
    _description = 'Dự án Xây Dựng'

    name = fields.Char('Tên dự án', required=True)
    partner_id = fields.Many2one('res.partner', string='Khách hàng')
    stock_picking_ids = fields.One2many('stock.picking', 'project_id', string='Lô hàng')
    invoice_ids = fields.One2many('account.move', 'project_id', string='Hóa đơn')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one('construction.project', string='Dự án liên quan')

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('construction.project', string='Dự án liên quan')

