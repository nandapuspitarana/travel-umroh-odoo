import logging
from odoo import models, fields, api


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Paket Travel Umroh"

    ref = fields.Char(string='Referensi', readonly=True, default='-')
    tanggal_berangkat = fields.Date('Tanggal Berangkat')
    tanggal_kembali = fields.Date('Tanggal Kembali')

    product_id = fields.Many2one('product.product', string='Sale', domain=[
                                 ('type', '=', "service")])
    package_id = fields.Many2one('product.product', string='Package')

    quota = fields.Integer('Quota')
    remaining_quota = fields.Integer('Remaining Quota')
    quota_progress = fields.Float('Quota Progress')

    # header button
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), (
        'done', 'Done')], string='Status', readonly=True, default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_cancel_confirm(self):
        self.write({'state': 'draft'})

    def action_close(self):
        self.write({'state': 'done'})

    def action_cancel_close(self):
        self.write({'state': 'confirm'})

    # notebook
    # hotel lines
    hotel_lines = fields.One2many('hotel.line', 'hotel_id', 'Nama Hotel')

    # airlines
    airline_lines = fields.One2many(
        'airline.line', 'airline_id', 'Nama Airline')

    # scheduled
    scedule_lines = fields.One2many(
        'scedule.line', 'scedule_id', 'Nama Kegiatan')

    # manifest
    manifest_lines = fields.One2many(
        'manifest.line', 'manifest_id', 'Manifest')

    # hpp
    hpp_lines = fields.One2many('hpp.line', 'travel_id', string='hpp')

    @api.onchange('package_id')
    def _onchange_package_id(self):

        for paket in self:
            isipaket = [(5, 0, 0)]

            for daftar in paket.package_id.bom_ids.bom_line_ids:
                komponen = {
                    'product_id': daftar.product_id.id,
                    'quantity': 1,
                    'unit_id': daftar.product_uom_id.id,
                    'unitprice': daftar.product_id.list_price,
                }

                isipaket.append((0, 0, komponen))
            paket.hpp_lines = isipaket


class HotelLine(models.Model):
    _name = 'hotel.line'

    hotel_id = fields.Many2one(
        'travel.package', 'Hotel Reference', required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner', 'Nama Hotel',
        domain=[('hotels', '=', True)]
    )
    city = fields.Char('City')
    check_in = fields.Date('Check In')
    check_out = fields.Date('Check Out')

    @api.onchange('partner_id')
    def onchange_hotel_id(self):
        if self.partner_id:
            self.city = self.partner_id.city


class AirlineLine(models.Model):
    _name = 'airline.line'

    airline_id = fields.Many2one(
        'travel.package', 'Airline Reference', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Nama Airline', domain=[
                                 ('airlines', '=', True)])
    tanggal_berangkat = fields.Date('Tanggal Berangkat')
    kota_asal = fields.Char('Kota Asal')
    kota_tujuan = fields.Char('Kota Tujuan')


class SceduleLine(models.Model):
    _name = 'scedule.line'

    scedule_id = fields.Many2one(
        'travel.package', 'Airline Reference', required=True, ondelete='cascade')
    kegiatan = fields.Char('Nama Kegiatan')
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan')


class ManifestLine(models.Model):
    _name = 'manifest.line'

    manifest_id = fields.Many2one(
        'travel.package', 'Manifest Reference')
    partner_id = fields.Many2one(
        'res.partner', string='', delegate=True)


class HPPLine(models.Model):
    _name = 'hpp.line'

    travel_id = fields.Many2one('travel.package', string='hpp')
    product_id = fields.Many2one('product.product', string='Barang')
    quantity = fields.Integer('Quantity')
    unit_id = fields.Many2one('uom.uom', string='Unit(s)')
    unitprice = fields.Float('unitprice')
    subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal')

    @api.depends('quantity', 'unitprice')
    def _compute_subtotal(self):
        _logger = logging.getLogger("===============")

        for price in self:
            price.subtotal = 0
            if price.quantity > 0 and price.unitprice > 0:
                price.subtotal = price.quantity * price.unitprice
                _logger.warning(msg=price.subtotal)
