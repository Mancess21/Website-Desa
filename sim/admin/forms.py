from sqlite3 import Timestamp
from tkinter.tix import Form
from xmlrpc.client import DateTime
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

from sim.models import Tpenduduk

class penduduk_F(FlaskForm):
    no_ktp = StringField('No KTP', validators=[DataRequired()])
    no_kk = StringField('No KK', validators=[DataRequired()])
    nama = StringField('NAMA', validators=[DataRequired()])
    tgl_lahir = StringField('TAGAL LAHIR', validators=[DataRequired()])
    j_kelamin = SelectField(u'Pilih Kelamin', choices=[('LakiLaki', 'Laki - Laki'), ('Perempuan', 'Perempuan')], validators=[DataRequired()])
    agama = SelectField(u'Pilih Agama', choices=[('Islam', 'Islam'), ('Kristen', 'Kristen'), ('Hindu', 'Hindu'), ('Budha', 'Budha'), ('Konghucu', 'Konghucu')], validators=[DataRequired()])
    pendidikan = SelectField(u'Pilih Pendidikan', choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA')], validators=[DataRequired()])
    pekerjaan = TextAreaField('Pekerjaan',validators=[DataRequired()])
    alamat = TextAreaField('Alamat',validators=[DataRequired()])
    RT = StringField('RT', validators=[DataRequired()])
    RW = StringField('RW', validators=[DataRequired()])
    s_nikah = SelectField(u'Pilih Nikah', choices=[('SudahNikah', 'Sudah Nikah'), ('BelumNikah', 'Belum Nikah')], validators=[DataRequired()])
    kewarganegaraan = SelectField(u'Pilih Kewarganegaraan', choices=[('WNA', 'WNA'), ('WNI', 'WNI')], validators=[DataRequired()])
    submit = SubmitField('Tambah')

class ependuduk_F(FlaskForm):
    no_ktp = StringField('No KTP', validators=[DataRequired()])
    no_kk = StringField('No KK', validators=[DataRequired()])
    nama = StringField('NAMA', validators=[DataRequired()])
    tgl_lahir = StringField('TAGAL LAHIR', validators=[DataRequired()])
    j_kelamin = SelectField(u'Pilih Kelamin', choices=[('LakiLaki', 'Laki - Laki'), ('Perempuan', 'Perempuan')], validators=[DataRequired()])
    agama = SelectField(u'Pilih Agama', choices=[('Islam', 'Islam'), ('Kristen', 'Kristen'), ('Hindu', 'Hindu'), ('Budha', 'Budha'), ('Konghucu', 'Konghucu')], validators=[DataRequired()])
    pendidikan = SelectField(u'Pilih Pendidikan', choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA')], validators=[DataRequired()])
    pekerjaan = TextAreaField('Pekerjaan',validators=[DataRequired()])
    alamat = TextAreaField('Alamat',validators=[DataRequired()])
    RT = StringField('RT', validators=[DataRequired()])
    RW = StringField('RW', validators=[DataRequired()])
    s_nikah = SelectField(u'Pilih Nikah', choices=[('SudahNikah', 'Sudah Nikah'), ('BelumNikah', 'Belum Nikah')], validators=[DataRequired()])
    kewarganegaraan = SelectField(u'Pilih Kewarganegaraan', choices=[('WNA', 'WNA'), ('WNI', 'WNI')], validators=[DataRequired()])
    submit = SubmitField('Ubah')


class surat_F(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    nik = SelectField('Nik',choices=[], validators=[DataRequired()])
    jenis_surat = SelectField(u'Pilih Surat', choices=[('SURAT KETERANGAN TIDAK MAMPU', 'SURAT KETERANGAN TIDAK MAMPU'), (
        'SURAT KETERANGAN DOMISILI', 'SURAT KETERANGAN DOMISILI'),('SURAT KETERANGAN BELUM MENIKAH', 'SURAT KETERANGAN BELUM MENIKAH'),('SURAT KETERANGAN KELAHIRAN', 'SURAT KETERANGAN KELAHIRAN'),('SURAT KETERANGAN BELUM MENIKAH', 'SURAT KETERANGAN KEMATIAN')], validators=[DataRequired()])
    keperluan = TextAreaField('Keperluan', validators=[DataRequired()])
    submit = SubmitField('Kirim')

class esurat_F(FlaskForm):
    no_surat = TextAreaField('Surat', validators=[DataRequired()])
    nik = TextAreaField('Surat', validators=[DataRequired()])
    jenis_surat = SelectField(u'Pilih Surat', choices=[('KurangMampu', 'Surat Kurang Mampu'), (
        'BelumMenika', 'Surat Belum Menika'),('Kematian', 'Surat Kematian')], validators=[DataRequired()])
    submit = SubmitField('ubah')



class login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class admin_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    konf_pass = PasswordField('Konfirmasi Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Login')


class profil_F(FlaskForm):
    nama_desa = TextAreaField('Nama Desa', validators=[DataRequired()])
    visi = TextAreaField('Visi', validators=[DataRequired()])
    misi = TextAreaField('Misi', validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    sejarah = TextAreaField('Sejarah', validators=[DataRequired()])
    peraturan = TextAreaField('Peraturan', validators=[DataRequired()])
    geografis = TextAreaField('Geografis', validators=[DataRequired()])
    kontak = TextAreaField('Kontak', validators=[DataRequired()])
    submit = SubmitField('Post')


class eprofil_F(FlaskForm):
    nama_desa = CKEditorField('Nama Desa')
    visi = CKEditorField('Visi')
    misi = CKEditorField('Misi')
    alamat = CKEditorField('Alamat')
    sejarah = CKEditorField('Sejarah')
    peraturan = CKEditorField('Peraturan')
    geografis = CKEditorField('Geografis')
    kontak = TextAreaField('Kontak')
    submit = SubmitField('Ubah')

class DataDemog_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    jumlah_l = StringField('Jumlah Laki-Laki', validators=[DataRequired()])
    jumlah_p = StringField('Jumlah Perempuan', validators=[DataRequired()])
    laju_pertumbuhan = StringField(
        'Laju Pertumbuhan', validators=[DataRequired()])
    submit = SubmitField('Tambah')

class edit_datademog_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    jumlah_l = StringField('Jumlah Laki-Laki', validators=[DataRequired()])
    jumlah_p = StringField('Jumlah Perempuan', validators=[DataRequired()])
    laju_pertumbuhan = StringField(
        'Laju Pertumbuhan', validators=[DataRequired()])
    submit = SubmitField('Ubah')





class putus_sekolah_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    sd = StringField('SD', validators=[DataRequired()])
    smp = StringField('SMP', validators=[DataRequired()])
    sma = StringField('SMA', validators=[DataRequired()])
    submit = SubmitField('kirim')

class eputus_sekolah_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    sd = StringField('SD', validators=[DataRequired()])
    smp = StringField('SMP', validators=[DataRequired()])
    sma = StringField('SMA', validators=[DataRequired()])
    submit = SubmitField('ubah')


class pendidikan_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    tdk_sd = StringField('Tidak SD', validators=[DataRequired()])
    tamat_sd = StringField('Tamat SD', validators=[DataRequired()])
    tamat_smp = StringField('Tamat SMP', validators=[DataRequired()])
    tamat_sma = StringField('Tamat SMA', validators=[DataRequired()])
    tamat_s1 = StringField('Tamat S1', validators=[DataRequired()])
    tamat_s2 = StringField('Tamat S2', validators=[DataRequired()])
    submit = SubmitField('kirim')

class ependidikan_F(FlaskForm):
    tahun = StringField('Tahun', validators=[DataRequired()])
    tdk_sd = StringField('Tidak SD', validators=[DataRequired()])
    tamat_sd = StringField('Tamat SD', validators=[DataRequired()])
    tamat_smp = StringField('Tamat SMP', validators=[DataRequired()])
    tamat_sma = StringField('Tamat SMA', validators=[DataRequired()])
    tamat_s1 = StringField('Tamat S1', validators=[DataRequired()])
    tamat_s2 = StringField('Tamat S2', validators=[DataRequired()])
    submit = SubmitField('ubah')


class prasarana_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    lokasi = TextAreaField('Lokasi', validators=[DataRequired()])
    status = TextAreaField('Status/Luar', validators=[DataRequired()])
    tahun_berdiri = StringField('Tahun Berdiri', validators=[DataRequired()])
    kategori = SelectField('Kategori Pendidikan', choices=[('SD', 'SD'), ('SMp', 'SMP'), ('SMA', 'SMA'), ('RumahIbadah', 'Rumah Ibadah'), ('SaranaOlahraga', 'Sarana Olahraga'), ('SaranaKesehatan', 'Sarana Kesehatam')], validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    foto=FileField('Foto', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Kirim')


class eprasarana_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    lokasi = TextAreaField('Lokasi', validators=[DataRequired()])
    status = SelectField('Status/Luar', validators=[DataRequired()])
    tahun_berdiri = TextAreaField('Tahun Berdiri', validators=[DataRequired()])
    kategori = SelectField('Kategori Pendidikan', choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA'), ('RumahIbadah', 'Rumah Ibadah'), ('SaranaOlahraga', 'Sarana Olahraga'), ('SaranaKesehatan', 'Sarana Kesehatam')], validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    foto=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('ubah')


class wisatawan_kuliner_F(FlaskForm):
    nama=StringField('Nama', validators=[DataRequired()])
    lokasi=TextAreaField('Lokasi', validators=[DataRequired()])
    kategori = SelectField('Kategori', choices=[('wisata alam','Wisata alam'),('wisata kuliner','Wisata kuliner'),('Wisata sejarah','Wisata Sejarah'),('adat & budaya','Adat & Budaya')],validators=[DataRequired()])
    status = SelectField('Status Kepemilikan', choices=[('Swasata','Swasta'),('Pemerintah','Pemerintah')],validators=[DataRequired()])
    nama_pemilik=StringField('Nama Pemilik', validators=[DataRequired()])
    deskripsi=TextAreaField('Deskripsi', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png']), DataRequired()])
    video=FileField('Video', validators=[FileAllowed(['mp4'])])
    submit = SubmitField('Tambah')


class ewisatawan_kuliner_F(FlaskForm):
    nama=StringField('Nama', validators=[DataRequired()])
    lokasi=TextAreaField('Lokasi', validators=[DataRequired()])
    kategori = SelectField('Kategori', choices=[('wisata alam','Wisata alam'),('wisata kuliner','Wisata kuliner'),('Wisata sejarah','Wisata Sejarah'),('adat & budaya','Adat & Budaya')],validators=[DataRequired()])
    status = SelectField('Status Kepemilikan', choices=[('Swasata','Swasta'),('Pemerintah','Pemerintah')],validators=[DataRequired()])
    nama_pemilik=StringField('Nama Pemilik', validators=[DataRequired()])
    deskripsi=TextAreaField('Deskripsi', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    video=FileField('Video', validators=[FileAllowed(['mp4'])])
    submit = SubmitField('ubah')

class kabar_desa_F(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired()])
    kategori = SelectField('Kategori Desa', choices=[('Berita', 'Berita Desa'), ('Agenda', 'Agenda Desa')], validators=[DataRequired()])
    deskripsi = StringField('Deskripsi', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    video=FileField('Video', validators=[FileAllowed(['mp4'])])
    submit = SubmitField('Tambah')


class ekabar_desa_F(FlaskForm):
    judul = TextAreaField('Judul', validators=[DataRequired()])
    kategori = SelectField('Kategori Desa', choices=[('Berita', 'Berita Desa'), ('agenda', 'Agenda Desa')], validators=[DataRequired()])
    deskripsi = StringField('Deskripsi', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    video=FileField('Video', validators=[FileAllowed(['mp4'])])
    submit = SubmitField('ubah')


class perangkat_desa_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    jabatan = StringField('Jabatan', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Tambah')


class eperangkat_desa_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    jabatan = StringField('Jabatan', validators=[DataRequired()])
    gambar=FileField('Gambar', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('ubah')

