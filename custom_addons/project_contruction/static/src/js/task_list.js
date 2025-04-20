odoo.define('project_construction.TaskList', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        _onRowClicked: function (ev) {
            var $row = $(ev.currentTarget);
            var id = $row.data('id');
            if (id && this.model === 'task.construction') {
                this.trigger_up('open_record', {id: id, target: 'current'});
                return;
            }
            return this._super.apply(this, arguments);
        },
    });
});