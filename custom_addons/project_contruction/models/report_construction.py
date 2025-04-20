from odoo import models, fields, api

class ReportConstruction(models.Model):
    _name = 'report.construction'
    _description = 'Báo cáo Dự Án'
    _rec_name = 'project_id'  # Hiển thị tên dự án thay vì ID

    name = fields.Char(string='Report Name',compute="_compute_name", store=True)
    project_id = fields.Many2one('project.construction', string="Project",compute="_compute_project_id", store=True)
    total_task_count = fields.Integer(string="Tổng số công việc", compute="_compute_task_count", store=True)
    delay_task_count = fields.Integer(string="Công việc đang trễ", compute="_compute_delay_task_count", store=True)
    done_task_count = fields.Integer(string="Công việc hoàn thành", compute="_compute_done_task_count", store=True)
    done_late_task_count = fields.Integer(string="Công việc hoàn thành trễ", compute="_compute_done_late_task_count", store=True)

    progress = fields.Float(string="Tiến độ (%)", compute="_compute_progress", store=True)

    _sql_constraints = [
        ('unique_project_report', 'UNIQUE(project_id)', 'Mỗi dự án chỉ có một báo cáo!')
    ]

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('done', 'Hoàn thành'),
    ], string="Trạng thái", default='draft')

    _sql_constraints = [
        ('unique_project_report', 'UNIQUE(project_id)', 'Mỗi dự án chỉ có một báo cáo!')
    ]

    # @api.depends('project_id.task_ids.status_task')
    # def _compute_task_count(self):
    #     for record in self:
    #         tasks = record.project_id.task_ids
    #         record.total_task_count = len(tasks)
    #         record.done_task_count = sum(1 for t in tasks if t.status_task == "Done")
    #         record.delay_task_count = sum(1 for t in tasks if t.status_task == "Delay")
    #         record.done_late_task_count = sum(1 for t in tasks if t.status_task == "Done late")
    #         record.progress = (record.done_task_count / record.total_task_count * 100) if record.total_task_count else 0


        
