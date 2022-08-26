from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    package_id = fields.Many2one('travel.package', string='Paket Perjalanan', domain=[
                                 ('state', '=', 'confirm')])

    # manifest
    manifest_lines = fields.One2many(
        'manifest.line', 'manifest_id', 'Manifest')

    manifest_sale_order_lines = fields.One2many(
        'manifest.sale.order.line', 'order_id', string='Manifest Sale Order')

    @api.onchange('package_id')
    def onchange_package_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.package_id.product_id:
                val = {
                    'product_id': line.id,
                    'name': line.name,
                    'product_uom_qty': 1,
                    'product_uom': line.uom_id,
                    'price_unit': line.list_price,
                    'tax_id': '',
                    'price_subtotal': 1 * line.list_price
                }
                lines.append((0, 0, val))
            rec.order_line = lines


class ManifestSaleOrderLine(models.Model):
    _name = 'manifest.sale.order.line'

    partner_id = fields.Many2one('res.partner', 'Nama Jamah', delegate=True)
    order_id = fields.Many2one('sale.order', string='order')
    tipe_kamar = fields.Selection([
        ('double', 'Double'), ('triple', 'Triple'), ('quad', 'Quad')
    ], string='Tipe Kamar')

    # mahrom_id = fields.Many2one('res.partner', string='Mahrom')
