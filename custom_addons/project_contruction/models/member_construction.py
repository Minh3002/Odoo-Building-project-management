from odoo import models, fields, api

class MemberConstruction(models.Model):
    _name = 'member.construction'
    _description = 'Construction member'

    name = fields.Char(string="Tên thành viên", compute="_compute_name", store=True)
    project_id = fields.Many2one('project.construction', string='Dự án', ondelete='cascade')
    member_id = fields.Many2one('res.users', string='Thành viên', ondelete='cascade', required=True)
    position_id = fields.Many2one('position.construction', string='Vị trí', ondelete='cascade', required=True, domain="[('name', '!=', 'QUản lý dự án')]")

    total_task_count = fields.Integer(string="Tổng số công việc",  compute="_compute_calculate_task", store=True)
    delay_task_count = fields.Integer(string="Công việc đang trễ",  compute="_compute_calculate_task", store=True)
    done_task_count = fields.Integer(string="Công việc hoàn thành",  compute="_compute_calculate_task", store=True)
    done_late_task_count = fields.Integer(string="Công việc hoàn thành trễ",  compute="_compute_calculate_task", store=True)

    progress = fields.Float(string="Tiến độ (%)" , default=0)

    @api.depends('project_id.task_ids', 'project_id.task_ids.assigned_members', 'project_id.task_ids.status_task')
    def _compute_calculate_task(self):
        for member in self:
            if (not member.project_id): continue
            tasks = self.env['task.construction'].search([
                ('project_id', '=', member.project_id.id),
                ('assigned_members', 'in', [member.id])
            ])
            if( len(tasks) == 0):
                member.total_task_count = 0
                member.delay_task_count = 0
                member.done_task_count = 0
                member.done_late_task_count = 0
            
            else:
                member.total_task_count = len(tasks)
                member.delay_task_count = len(tasks.filtered(lambda t: t.status_task == 'Delay'))
                member.done_task_count = len(tasks.filtered(lambda t: t.status_task == 'Done' or t.status_task == 'Done late'))
                member.done_late_task_count = len(tasks.filtered(lambda t: t.status_task == 'Done late'))
                member.progress = member.done_task_count / member.total_task_count

    @api.depends('member_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.member_id.name} - {record.position_id.name}" if record.member_id else "Chưa có tên"
