from odoo import models, fields

class TaskConstruction(models.Model):
    _name = 'task.construction'
    _description = 'Construction Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)

    status_task = fields.Selection([
        ('On track', 'Đã thực hiện'),
        ('Done', 'Trễ tiến độ'),
        ('Delay', ''),
        ('Done late', 'Hoàn thành muộn')
    ], string="Trạng thái công việc", default='On track')
    
    attachment_ids = fields.Many2many(
        'ir.attachment', string='Attachments',
        relation='task_construction_attachment_rel',
        column1='task_id', column2='attachment_id'
    )

    sub_task_ids = fields.One2many('task.construction', 'parent_task_id', string='Sub Tasks')
    parent_task_id = fields.Many2one('task.construction', string='Parent Task', ondelete='cascade')

    member_ids = fields.Many2many('res.users', string='Members')

    project_id = fields.Many2one('project.construction', string='Project', ondelete='cascade' )

