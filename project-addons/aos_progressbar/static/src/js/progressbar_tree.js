odoo.define('progressbar_tree.ColumnProgressBar', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var Widget = require('web.Widget');
var ListView = require('web.ListView');
var Model = require('web.DataModel');

var QWeb = core.qweb;
var _t = core._t;
var list_widget_registry = core.list_widget_registry;

var ColumnProgressBar = ListView.Column.extend({
    _format: function (row_data, options) {
        return _.template(
            '<div class="background-color: #ddd;valign: middle;"><div style="width:<%-value%>%;background-color: #2196F3;text-align: center;color: white;" value="<%-value%>" max="100"><%-value%>%</div></div>')({
                value: _.str.sprintf("%.2f", row_data[this.id].value || 0)
            });
    }
});

list_widget_registry.add('field.progressbar', ColumnProgressBar);

});
