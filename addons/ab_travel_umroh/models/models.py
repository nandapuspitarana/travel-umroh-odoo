import logging
from odoo import models, fields, api

_logger = logging.getLogger("====models====")


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Paket Travel Umroh"

    # generate sequence referensi berdasarkan sequence_data.xml
    ref = fields.Char(string='Referensi', readonly=True, default='-')

    tanggal_berangkat = fields.Date('Tanggal Berangkat', required=True)
    tanggal_kembali = fields.Date('Tanggal Kembali', required=True)

    # untuk manmpilkan produk yang akan di ambil
    # ini juga generate name travel package berdasarkan dep sale
    product_id = fields.Many2one('product.product', required=True, string='Sale', domain=[
                                 ('type', '=', "service")])

    package_id = fields.Many2one(
        'product.product', required=True, string='Package')

    quota = fields.Integer('Quota', required=True)
    remaining_quota = fields.Integer('Remaining Quota')
    quota_progress = fields.Float('Quota Progress')

    # notebook
    # hotel lines
    hotel_lines = fields.One2many(
        'hotel.line', 'hotel_id', 'Nama Hotel', required=True)

    # airlines
    airline_lines = fields.One2many(
        'airline.line', 'airline_id', 'Nama Airline', required=True)

    # scheduled
    schedule_lines = fields.One2many(
        'scedule.line', 'scedule_id', 'Nama Kegiatan', required=True)

    # manifest
    manifest_lines = fields.One2many(
        'manifest.line', 'manifest_id', 'Manifest')

    # hpp
    hpp_lines = fields.One2many('hpp.line', 'travel_id', string='hpp')

    # total cost
    total_cost = fields.Float(
        compute='_compute_total_cost', string='Total Cost')

    # header button
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), (
        'done', 'Done')], string='Status', readonly=True, default='draft')

    # update jamaah
    order_id = fields.One2many('sale.order', 'package_id', 'Order', domain=[
                               ('state', 'ilike', 'sale')])

    # update jamaah
    def action_update_jamaah(self):
        self.remaining_quota = self.quota - \
            len(self.order_id.manifest_sale_order_lines)
        self.quota_progress = 100 * \
            len(self.order_id.manifest_sale_order_lines) / self.quota
        for rec in self:
            lines = [(5, 0, 0)]
            env = self.env['sale.order'].search(
                [('package_id', '=', self.id), ('state', '=', 'sale')])
            for line in env:
                _logger.warning(line.manifest_sale_order_lines)
                for manifestjamaah in line.manifest_sale_order_lines:
                    val = {
                        'partner_id': manifestjamaah.partner_id.id,
                        # 'tipe_kamar': a.tipe_kamar,
                        # 'umur': a.umur,
                        # 'mahrom': a.mahrom.id

                        # 'title': line.partner_id.title.name,
                        # 'nama_paspor': line.partner_id.nama_paspor,
                        # 'jenis_kelamin': line.partner_id.jenis_kelamin,
                        # 'no_ktp': line.partner_id.no_ktp,
                        # 'no_paspor': line.partner_id.no_paspor,
                        # 'tanggal_lahir': line.partner_id.tanggal_lahir,
                        # 'tempat_lahir': line.partner_id.tempat_lahir,
                        # 'tanggal_berlaku': line.partner_id.tanggal_berlaku,
                        # 'tanggal_expired': line.partner_id.tanggal_expired,
                        # 'imigrasi': line.partner_id.imigrasi,
                        # 'tipe_kamar': line.tipe_kamar,
                        # 'umur': line.umur,
                        # 'mahrom': line.mahrom.id
                    }
                    lines.append((0, 0, val))
                rec.manifest_lines = lines

    # header button
    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_cancel_confirm(self):
        self.write({'state': 'draft'})

    def action_close(self):
        self.write({'state': 'done'})

    def action_cancel_close(self):
        self.write({'state': 'confirm'})

    # generate name travel package berdasarkan dep sale
    def name_get(self):
        result = []
        for ab in self:
            ref = ab.ref + ' - ' + ab.product_id.name
            result.append((ab.id, ref))
        return result

    # generate sequence referensi berdasarkan sequence_data.xml
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)

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

    @api.depends('hpp_lines')
    def _compute_total_cost(self):
        for total in self:
            totals = 0
            for reg in self.hpp_lines:
                totals += reg.subtotal
            total.total_cost = totals

    @api.onchange('quota')
    def onchange_quota(self):
        self.remaining_quota = self.quota - len(self.manifest_lines)
        if self.quota and self.manifest_lines:
            self.quota_progress = 100 * len(self.manifest_lines) / self.quota


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
        for price in self:
            price.subtotal = 0
            if price.quantity > 0 and price.unitprice > 0:
                price.subtotal = price.quantity * price.unitprice
