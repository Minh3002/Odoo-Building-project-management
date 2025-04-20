
from odoo import models, fields, api

class ProjectConstruction(models.Model):
    _name = 'project.construction'
    _description = 'Project Construction'

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Description')

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    actual_date_end = fields.Date(string='Actual End Date')
    leader_id = fields.Many2one('res.users', string='Quản lý dự án', ondelete='cascade')

    location = fields.Char(string='Location', required=True)
    scale= fields.Char(string='Scale', required=True)
    area = fields.Float(string='Area (m2)', required=True)

    budget_amount = fields.Float(string="Tổng ngân sách", compute="_compute_spent_amount", store=True)
    spent_amount = fields.Float(string="Đã chi", compute="_compute_spent_amount", store=True)
    costs_incurred = fields.Float(string="Đã chi", compute="_compute_spent_amount", store=True)
    remaining_budget = fields.Float(string="Ngân sách còn lại", compute="_compute_spent_amount", store=True)

    total_task_count = fields.Integer(string="Tổng số công việc", compute="_compute_count_task", store=True)
    delay_task_count = fields.Integer(string="Công việc đang trễ", compute="_compute_count_delay", store=True)
    done_task_count = fields.Integer(string="Công việc hoàn thành", compute="_compute_count_done", store=True)
    done_late_task_count = fields.Integer(string="Công việc hoàn thành trễ", compute="_compute_count_done_late", store=True)

    progress = fields.Float(string="Tiến độ (%)",compute="_compute_progress_project", store=True)

    status_construction = fields.Selection([
        ('Planned', 'Đã lên kế hoạch'),
        ('On Hold', 'Tạm dừng'),
        ('Under Construction', 'Đang thi công'),
        ('Cancelled', 'Đã hủy'),
        ('Completed', 'Hoàn thành'),
        ('Testing & Commissioning', ' Kiểm tra & nghiệm thu'),
        ('Handover', 'Bàn giao'),
    ], string="Trạng thái dự án", default='Planned')

    category = fields.Many2one('category.construction', string="Category", required=True)

    task_ids = fields.One2many('task.construction', 'project_id', string='Task Construction')

    member_ids = fields.One2many('member.construction', 'project_id', string="Project Members")

    risk_ids = fields.One2many('risk.construction', 'project_id', string='Risk Construction')

    document_ids = fields.One2many('document.construction', 'project_id', string='Document Construction')

    safety_ids = fields.One2many('safety.construction', 'project_id', string='Safety Construction')

    contract_ids = fields.One2many('contract.construction', 'project_id', string='Contract Construction')

    budget_ids = fields.One2many('budget.construction', 'project_id', string="Danh sách chi tiêu")

    stock_ids = fields.One2many('stock.construction', 'project_id', string="Danh sách vật tư")

    @api.model
    def create(self, vals):
        project = super(ProjectConstruction, self).create(vals)

        if project.leader_id:
            self._create_project_member(project)

        return project

    def _create_project_member(self, project):
        member_obj = self.env['member.construction']
        position = self.env['position.construction'].search([('name', '=', 'Quản lý dự án')], limit=1)
        # Tạo mới member cho dự án
        member_obj.create({
            'project_id': project.id,
            'position_id' : position.id,
            'member_id': project.leader_id.id,
        })

    @api.depends('budget_ids.spent_amount', 'budget_ids.amount_type')
    def _compute_spent_amount(self):
        for project in self:
            # Tính tổng ngân sách
            if project.budget_ids:
                budget_additional = sum(project.budget_ids.filtered(lambda b: b.amount_type == 'additional budget').mapped('spent_amount'))
                # budget_initial = sum(project.budget_ids.filtered(lambda b: b.amount_type != 'additional budget').mapped('total_amount'))  # Giả sử có field total_amount

                project.budget_amount = budget_additional

                # Tính tổng chi tiêu (không tính khoản bổ sung)
                total_spent = sum(project.budget_ids.filtered(lambda b: b.amount_type != 'additional budget').mapped('spent_amount'))
                project.spent_amount = total_spent

                costs_incurred = sum(project.budget_ids.filtered(lambda b: b.amount_type == 'costs incurred').mapped('spent_amount'))

                # Ngân sách còn lại
                project.remaining_budget = max(project.budget_amount - total_spent, 0)

                project.costs_incurred = costs_incurred
            
    @api.depends('task_ids')
    def _compute_count_task(self):
        for project in self:
            project.total_task_count = len(project.task_ids)

    @api.depends('task_ids.status_task')
    def _compute_count_delay(self):
        for project in self:
            project.delay_task_count = len(project.task_ids.filtered(lambda t: t.status_task == 'Delay'))

    @api.depends('task_ids.status_task')
    def _compute_count_done(self):
        for project in self:
            project.done_task_count = len(project.task_ids.filtered(lambda t: t.status_task == 'Done' or t.status_task == 'Done late'))

    @api.depends('task_ids.status_task')
    def _compute_count_done_late(self):
        for project in self:
            project.done_late_task_count = len(project.task_ids.filtered(lambda t: t.status_task == 'Done late'))

    @api.depends('task_ids.status_task')
    def _compute_progress_project(self):
        for project in self:
            if project.total_task_count > 0:
                project.progress = project.done_task_count/project.total_task_count

    def action_open_task_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'task.construction',
            'view_mode': 'form',
            'target': 'current',  # Mở trong cửa sổ hiện tại
            'context': {
                'default_project_id': self.id,
                'form_view_ref': 'your_module.view_task_construction_form'
            },
        }