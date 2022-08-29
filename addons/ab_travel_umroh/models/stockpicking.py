from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one('res.partner', 'Nama')
    move_lines = fields.One2many('stock.move', 'picking_id', 'Stock Moves')
    logged_user = fields.Many2one(
        'res.users', string='Current User', default=lambda self: self.env.uid)

    def action_print_delivery(self):
        return self.env.ref('ab_travel_umroh.report_stock_delivery_action').report_action(self)
