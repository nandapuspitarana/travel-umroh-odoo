from datetime import date
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    # additional information
    nomor_ktp = fields.Char(string="No. KTP")
    nama_ayah = fields.Char(string="Nama Ayah")
    pekerjaan_ayah = fields.Char(string="Pekerjaan Ayah")
    tempat_lahir = fields.Char(string="Tempat Lahir")
    pendidikan = fields.Selection(
        [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA'), ('s1', 'S1'), ('s2', 'S2')], string='Pendidikan')
    status_hubungan = fields.Selection(
        [('married', 'Married'), ('single', 'Single'), ('divorce', 'Divorce')], string='Status Hubungan')
    jenis_kelamin = fields.Selection(
        [('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin')
    nama_ibu = fields.Char(string="Nama Ibu")
    pekerjaan_ibu = fields.Char(string="Pekerjaan Ibu")
    tanggal_lahir = fields.Date(string="Tanggal Lahir")
    golongan_darah = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')], string='Golongan Darah')
    ukuran_baju = fields.Selection(
        [('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')], string='Ukuran Baju')

    # passport information
    no_paspor = fields.Char(string="No. Paspor")
    nama_paspor = fields.Char(string="Nama Paspor")
    tanggal_berlaku = fields.Date(string="Tanggal Berlaku")
    tanggal_expired = fields.Date(string="Tanggal Expired")
    imigrasi = fields.Char(string="Imigrasi")

    # Scan Document
    scan_paspor = fields.Binary(string="Scan Paspor")
    scan_buku_nikah = fields.Binary(string="Scan Buku Nikah")
    scan_ktp = fields.Binary(string="Scan KTP")
    scan_kk = fields.Binary(string="Scan Kartu Keluarga")

    # scan document
    airlines = fields.Boolean('Airlines')
    hotels = fields.Boolean('Hotel')

    # additional manifest
    umur = fields.Char(compute='_compute_umur', string='Umur')

    @api.depends('tanggal_lahir')
    def _compute_umur(self):
        umurs = date.today()
        for user in self:
            user.umur = 0
            if user.tanggal_lahir:
                user.umur = umurs.year - user.tanggal_lahir.year
