from odoo import api, fields, models


class ManifestXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_manifest_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Manifest')
        # styling paling atas
        text_top_style = workbook.add_format(
            {'font_size': 12, 'bold': True, 'font_color': 'black', 'valign': 'vcenter'})

        # styling header tabel
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True, 'font_color': 'white',
                                                'bg_color': '#28A27E', 'valign': 'vcenter', 'align': 'center'})
        text_style = workbook.add_format(
            {'font_size': 12, 'valign': 'vcenter', 'align': 'center'})

        # buat header paling atas baris 2 colom 3
        sheet.write(1, 2, "Manifest", text_top_style)
        # buat header paling atas baris 2 colom 4
        sheet.write(1, 3, obj.ref, text_top_style)

        # buat variabel header tabel awal di BARIS 4
        row = 3
        header = ['NO', 'TITLE', 'GENDER', 'FULLNAME', 'TEMPAT LAHIR', 'TANGGAL LAHIR', 'NO. PASSPOR', 'PASSPOR ISSUED',
                  'PASSPOR EXPIRED', 'IMIGRASI', 'MAHROM', 'USIA', 'NIK', 'ORDER', 'ROOM TYPE', 'ROOM LEADER', 'NO. ROOM', 'ALAMAT']
        # buat header tabel awal
        sheet.write_row(row, 0, header, text_header_style)

        # variabel body tabel
        no_list = []
        title = []
        gender = []
        fullname = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passpor = []
        passpor_issued = []
        passpor_expired = []
        imigrasi = []
        mahrom = []
        usia = []
        nik = []
        order = []
        room_type = []
        room_leader = []
        no_room = []
        alamat = []

        no = 1
        for x in obj.order_id.manifest_sale_order_lines:
            no_list.append(no)
            title.append(x.partner_id.title.name or '-')
            gender.append(x.partner_id.jenis_kelamin or '-')
            fullname.append(x.partner_id.name or '-')
            tempat_lahir.append(x.partner_id.tempat_lahir or '-')
            tanggal_lahir.append(
                x.partner_id.tanggal_lahir.strftime('%d-%m-%Y') or '-')
            no_passpor.append(x.partner_id.no_paspor or '-')
            passpor_issued.append(
                x.partner_id.tanggal_berlaku.strftime('%d-%m-%Y') or '-')
            passpor_expired.append(
                x.partner_id.tanggal_expired.strftime('%d-%m-%Y') or '-')
            imigrasi.append(x.partner_id.imigrasi or '-')
            mahrom.append(x.partner_id.mahrom_id.name or '-')
            usia.append(x.umur or '-')
            nik.append(x.partner_id.nomor_ktp or '-')
            order.append(x.order_id.name)
            room_type.append(x.tipe_kamar or '-')
            room_leader.append('-')
            no_room.append('-')
            alamat.append(x.partner_id.city or '-')
            no += 1

        row += 1
        sheet.write_column(row, 0, no_list, text_style)
        sheet.write_column(row, 1, title, text_style)
        sheet.write_column(row, 2, gender, text_style)
        sheet.write_column(row, 3, fullname, text_style)
        sheet.write_column(row, 4, tempat_lahir, text_style)
        sheet.write_column(row, 5, tanggal_lahir, text_style)
        sheet.write_column(row, 6, no_passpor, text_style)
        sheet.write_column(row, 7, passpor_issued, text_style)
        sheet.write_column(row, 8, passpor_expired, text_style)
        sheet.write_column(row, 9, imigrasi, text_style)
        sheet.write_column(row, 10, mahrom, text_style)
        sheet.write_column(row, 11, usia, text_style)
        sheet.write_column(row, 12, nik, text_style)
        sheet.write_column(row, 13, order, text_style)
        sheet.write_column(row, 14, room_type, text_style)
        sheet.write_column(row, 15, room_leader, text_style)
        sheet.write_column(row, 16, no_room, text_style)
        sheet.write_column(row, 17, alamat, text_style)

        # buat variabel header tabel awal di BARIS 5 + panjang baris manifest
        row_2 = len(obj.order_id.manifest_sale_order_lines)+5
        header = ['NO', 'AIRLINE', 'DEPARTURE DATE',
                  'DEPARTURE CITY', 'ARIVAL CITY']
        sheet.write_row(row_2, 2, header, text_header_style)

        no_list = []
        airline = []
        departure_date = []
        departure_city = []
        arival_city = []

        no_2 = 1
        for y in obj.airline_lines:
            no_list.append(no_2)
            airline.append(y.partner_id.name)
            departure_date.append(y.tanggal_berangkat.strftime('%d-%m-%Y'))
            departure_city.append(y.kota_asal)
            arival_city.append(y.kota_tujuan)
            no_2 += 1

        row_2 += 1
        sheet.write_column(row_2, 2, no_list, text_style)
        sheet.write_column(row_2, 3, airline, text_style)
        sheet.write_column(row_2, 4, departure_date, text_style)
        sheet.write_column(row_2, 5, departure_city, text_style)
        sheet.write_column(row_2, 6, arival_city, text_style)
