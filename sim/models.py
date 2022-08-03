from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint, null
from sim import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(admin_id):
    return Tadmin.query.get(int(admin_id))

# awal table admin


class Tadmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(6), nullable=False)

    def __repr__(self):
        return f"Tprofil('{self.nama}', '{self.username}', '{self.password}')"
# akhir table admin


# awal table demografi
class DataDemog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(5), nullable=False)
    jumlah_l = db.Column(db.String(5), nullable=False)
    jumlah_p = db.Column(db.String(5), nullable=False)
    laju_pertumbuhan = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"DataDemog('{self.tahun}','{self.jumlah_l}','{self.jumlah_p}','{self.laju_pertumbuhan}')"
# akhir table demografi

# awal table profil
class Tprofil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_desa = db.Column(db.Text, nullable=False)
    visi = db.Column(db.Text, nullable=False)
    misi = db.Column(db.Text, nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    sejarah = db.Column(db.Text, nullable=False)
    peraturan = db.Column(db.Text, nullable=False)
    geografis = db.Column(db.String(30))
    kontak = db.Column(db.Text, nullable=False)
    logo = db.Column(db.String(30))

    def __repr__(self):
        return f"Tprofil('{self.nama_desa}','{self.visi}','{self.misi}','{self.alamat}','{self.sejarah}','{self.peraturan}','{self.geografis}','{self.kontak}','{self.logo}'"
# akhir table profil

# awal table penduduk
@login_manager.user_loader
def load_user(penduduk_id):
    return Tpenduduk.query.get(int(penduduk_id))

class Tpenduduk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_ktp = db.Column(db.String(25), unique=True, nullable=True)
    no_kk = db.Column(db.String(25), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    tgl_lahir = db.Column(db.String(50), nullable=False)
    j_kelamin = db.Column(db.String(50), nullable=False)
    agama = db.Column(db.String(50), nullable=False)
    pendidikan = db.Column(db.String(100), nullable=False)
    pekerjaan = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    RT = db.Column(db.String(50), nullable=False)
    RW = db.Column(db.String(50), nullable=False)
    s_nikah = db.Column(db.String(300), nullable=False)
    kewarganegaraan = db.Column(db.String(50), nullable=False)
    hub_surat = db.relationship('Tsurat_ket', backref='penduduk', lazy=True)

    def __repr__(self):
        return f"Tpenduduk('{self.no_ktp}','{self.no_kk}','{self.nama}','{self.tgl_lahir}','{self.j_kelamin}','{self.agama}','{self.pendidikan}','{self.pekerjaan}','{self.alamat}', '{self.RT}','{self.RW}','{self.s_nikah}','{self.kewarganegaraan}')"
# akhir table penduduk

# Surat Keterangan
class Tsurat_ket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_surat = db.Column(db.String(50), nullable=False)
    jenis_surat = db.Column(db.String(300), nullable=False)
    keperluan = db.Column(db.String(100), nullable=False)
    penduduk_id = db.Column(db.Integer, db.ForeignKey('tpenduduk.id'))

    def __repr__(self):
        return f"Tsurat_ket('{self.no_surat}', '{self.jenis_surat}', '{self.keperluan}')"
# Akhir Table Keterangan


# Pendidikan
class Tpendidikan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.Text, nullable=False)
    tdk_sd = db.Column(db.Text, nullable=False)
    tamat_sd = db.Column(db.Text, nullable=False)
    tamat_smp = db.Column(db.Text, nullable=False)
    tamat_sma = db.Column(db.Text, nullable=False)
    tamat_s1 = db.Column(db.Text, nullable=False)
    tamat_s2 = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Tpendidikan('{self.tahun}','{self.tdk_sd}','{self.tamat_sd}','{self.tamat_smp}','{self.tamat_sma}','{self.tamat_s1}', '{self.tamat_s2}')"
# Akhir Table Pendidikan

# Putus Sekolah
class Tputus_sekolah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.Text, nullable=False)
    sd = db.Column(db.Text, nullable=False)
    smp = db.Column(db.Text, nullable=False)
    sma = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Tputus_sekolah('{self.tahun}','{self.sd}','{self.smp}','{self.sma}')"
# Akhir Putus Sekolah

# Prasarana
class Tprasarana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, nullable=False)
    lokasi = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    tahun_berdiri = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Tprasarana('{self.nama}','{self.lokasi}','{self.status}','{self.tahun_berdiri}','{self.kategori}','{self.foto}')"
# Akhir Table Prasarana









# Galeri
class Tgaleri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gambar = db.Column(db.String(30), nullable=True)
    video = db.Column(db.String(30), nullable=True)
    def __repr__(self):
        return f"Tgaleri('{self.gambar}','{self.video}')"
# Akhir Galeri


# Wisata
class Twisata_kuliner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, nullable=False)
    lokasi = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    nama_pemilik = db.Column(db.Text, nullable=True)
    deskripsi = db.Column(db.Text, nullable=True)
    gambar = db.Column(db.String(30), nullable=True)
    video = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Twisata_kuliner('{self.nama}','{self.lokasi}','{self.kategori}','{self.status}','{self.nama_pemilik}','{self.deskripsi}','{self.gambar}','{self.video}')"
# Akhir Tambel Wisata

# Petanda Desa
class Tpetanda_desa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, nullable=False)
    gambar = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Tpetanda_desa('{self.nama}','{self.gambar}')"
# Akhir Petanda Desa

# Kabar Desa
class Tkabar_desa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deskripsi = db.Column(db.Text, nullable=True)
    gambar = db.Column(db.String(30), nullable=True)
    video = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Twisata_kuliner('{self.judul}','{self.kategori}','{self.tanggal}','{self.deskripsi}','{self.gambar}','{self.video}')"
# Akhir Kabar Desa

# Perangkat Desa
class Tperangkat_desa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, nullable=False)
    jabatan = db.Column(db.Text, nullable=False)
    gambar = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"Tperangkat_desa('{self.nama}','{self.jabatan}','{self.gambar}')"
# Akhir Perangkat Desa



class Tpengaduan(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=False)
    subjek = db.Column(db.String(15), nullable=False)
    detail_pengaduan = db.Column(db.String(120), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Tpengaduan('{self.subjek}','{self.detail_pengaduan}','{self.tgl_post}')"