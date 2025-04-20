from odoo import models, fields, api

class TaskConstruction(models.Model):
    _name = 'task.construction'
    _description = 'Construction Task'
    _parent_name = "parent_task_id"
    _parent_store = True
    _order = 'parent_path, sequence, id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True, tracking=True)
    display_name = fields.Char(string='Công việc')
    description = fields.Text(string='Description', tracking=True)
    start_date = fields.Date(string='Ngày bắt đầu', tracking=True)
    end_date = fields.Date(string='Ngày hết hạn', tracking=True)
    sequence = fields.Integer(string='sequence stage', default=1)
    parent_path = fields.Char(index=True)
    outline_level = fields.Integer(string="level task")
    wbs = fields.Char(string="WBS", compute="_compute_wbs", store=True)

    status_task = fields.Selection([
        ('On track', 'Đang thực hiện'),
        ('Delay', 'Trễ tiến độ'),
        ('Done', 'Hoàn thành'),
        ('Done late', 'Hoàn thành muộn')
    ], string="Trạng thái công việc", default='On track')

    total_task_count = fields.Integer(string="Tổng số công việc con", compute="_compute_subtask_stats", store=True)
    delay_task = fields.Integer(string="Trễ", compute="_compute_subtask_stats", store=True)
    done_task = fields.Integer(string="Hoàn thành", compute="_compute_subtask_stats", store=True)
    done_late_task = fields.Integer(string="Hoàn thành trễ", compute="_compute_subtask_stats", store=True)
    progress = fields.Float(string="Tiến độ (%)", compute="_compute_progress_task", store=True)

    task_id = fields.Integer(string="ID")



    sub_task_ids = fields.One2many('task.construction', 'parent_task_id', string='Sub Tasks')

    parent_task_id = fields.Many2one('task.construction', string='Parent Task', ondelete='cascade')
    
    project_id = fields.Many2one('project.construction', string='Project', ondelete='cascade' )

    risk_ids = fields.One2many('risk.construction', 'task_id', string='Risk Construction')

    document_ids = fields.One2many('document.construction', 'task_id', string='Document Construction')

    safety_ids = fields.One2many('safety.construction', 'task_id', string='Safety Construction')

    contract_ids = fields.One2many('contract.construction', 'task_id', string='Contract Construction')

    budget_ids = fields.One2many('budget.construction', 'task_id', string="Danh sách chi tiêu")

    stock_ids = fields.One2many('stock.construction', 'task_id', string="Danh sách vật tư")

    assigned_members = fields.Many2many('member.construction',string="Assigned Members",domain="[('project_id', '=', project_id)]")
    
    def write(self, vals):
        if 'name' in vals:
            for task in self:
                new_name = vals['name']
                if task.parent_task_id:
                    # Nếu là task con, giữ nguyên cấu trúc thụt lề
                    vals['display_name'] = ('____     ' * (task.outline_level - 1)) + new_name
                else:
                    # Nếu là task cha, chỉ cập nhật tên
                    vals['display_name'] = new_name
        res = super(TaskConstruction, self).write(vals)
        if 'status_task' in vals or 'project_id' in vals:
            # Tìm tất cả project liên quan cần cập nhật
            project_ids = self.mapped('project_id').ids
            if project_ids:
                projects = self.env['project.construction'].browse(project_ids)
                projects._compute_count_task()
                projects._compute_count_delay()
                projects._compute_count_done()
                projects._compute_count_done_late()
        return res

    @api.onchange('parent_task_id')
    def _onchange_parent_task_id(self):
        if self.parent_task_id:
            self.project_id = self.parent_task_id.project_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            last_task = self.search([], order='task_id desc', limit=1)
            next_id = last_task.task_id + 1 if last_task else 1
            vals['task_id'] = next_id
            if vals.get('parent_task_id'):
                parent_task = self.env['task.construction'].browse(vals['parent_task_id'])
                vals['outline_level'] = parent_task.outline_level + 1
                vals['display_name'] = ('____ ' * (int(vals.get('outline_level', 0)) - 1)) + str(vals.get('name', ''))
                if parent_task.project_id:
                    vals['project_id'] = parent_task.project_id.id  

            else:
                vals['display_name'] = vals['name']
                vals['outline_level'] = 1

        tasks = super(TaskConstruction, self).create(vals_list)

        return tasks
    
    @api.depends("parent_task_id", "parent_task_id.wbs")
    def _compute_wbs(self):
        for task in self:
            if task.parent_task_id:
                # Chỉ sắp xếp các task đã có ID thực
                siblings = task.parent_task_id.sub_task_ids.filtered(lambda t: isinstance(t.id, int))
                siblings = siblings.sorted('id')
                
                # Xác định vị trí
                if isinstance(task.id, int):
                    task_index = siblings.ids.index(task.id) + 1
                else:
                    task_index = len(siblings) + 1
                    
                task.wbs = f"{task.parent_task_id.wbs}.{task_index}"
            else:
                # Tương tự cho task gốc
                root_tasks = self.search([
                    ('project_id', '=', task.project_id.id),
                    ('parent_task_id', '=', False),
                    ('id', '!=', task.id)
                ], order="id")
                if len(root_tasks) == 0:
                    task.wbs = 1
                    return
                if task.id:
                    task_index = root_tasks.ids.index(task.id) + 1 if task.id in root_tasks.ids else len(root_tasks) + 1
                else:
                    task_index = len(root_tasks) + 1
                task.wbs = str(task_index)

    @api.depends('status_task')
    def _compute_progress_task(self):
        for task in self:
            if len(task.sub_task_ids) > 0:
                return
            if task.status_task in ['Done', 'Done late']:
                    task.progress = 1.0
    
    @api.depends('sub_task_ids.status_task')
    def _compute_subtask_stats(self):
        for task in self:

            total = len(task.sub_task_ids)
            done = 0
            done_late = 0
            delay = 0

            for subtask in task.sub_task_ids:
                if subtask.status_task == 'Done':
                    done += 1
                if subtask.status_task == 'Done late':
                    done += 1
                    done_late += 1
                elif subtask.status_task == 'Delay':
                    delay += 1

            task.total_task_count = total
            task.done_task = done
            task.done_late_task = done_late
            task.delay_task = delay

            # Tính tiến độ theo % số task đã hoàn thành
            if total > 0:
                task.progress = round((done / total), 2)
            else:
                if task.status_task in ['Done', 'Done late']:
                    task.progress = 1.0
                else:
                    task.progress = 0.0
