import json
import logging
from odoo import models, fields, api

_logger = logging.getLogger("====models====")


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_id = fields.Many2one('res.partner', 'Nama')
    invoice_line_ids = fields.One2many(
        'account.move.line', 'move_id', 'Invoice Lines')
    payment_id = fields.Many2one(
        'account.payment', string="Account Payment")

    def action_cetak_invoice(self):
        return self.env.ref('aa_travel_umroh.report_cetak_invoice_action').report_action(self)

    def get_widget(self):
        ambil = json.loads(self.invoice_payments_widget)
        _logger.warning(ambil)
        if ambil:
            return ambil['content']
        return
