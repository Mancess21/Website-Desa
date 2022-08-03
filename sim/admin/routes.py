# from crypt import methods
import secrets
import os
from PIL import Image
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sim import db, bcrypt, app
from sim.admin.forms import ependidikan_F, eperangkat_desa_F, eputus_sekolah_F, login, pendidikan_F, perangkat_desa_F, profil_F, DataDemog_F, penduduk_F,ependuduk_F ,putus_sekolah_F, surat_F,esurat_F ,admin_F, eprofil_F, edit_datademog_F, wisatawan_kuliner_F,  ewisatawan_kuliner_F, kabar_desa_F, ekabar_desa_F, prasarana_F, eprasarana_F
from sim.models import Tpenduduk, Tperangkat_desa, Tprasarana, Tprofil, DataDemog, Tsurat_ket, Tadmin, Tpendidikan, Tprasarana, Tputus_sekolah, Tkabar_desa, Twisata_kuliner
# from sim.penduduk.routes import profil

Sadmin = Blueprint('Sadmin', __name__)


def simpan_foto(form_foto):
    random_hex=secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_foto.filename)
    foto_fn=random_hex + f_ext
    foto_path=os.path.join(app.root_path, 'sim/static/foto', foto_fn)
    ubah_size=(400,300)
    j=Image.open(form_foto)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn

def simpan_video(form_video):
    random_hex=secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_video.filename)
    video_fn=random_hex + f_ext
    video_path=os.path.join(app.root_path, 'sim/static/video', video_fn)
    ubah_size=(400,300)
    #j=Video.open(form_video)
    #j.thumbnail(ubah_size)
    #j.save(video_path)
    form_video.save(video_path)
    return video_fn


@Sadmin.route("/daftar_admin",  methods=['GET', 'POST'])
def daftar_admin():
    form = admin_F()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(
            form.password.data).decode('UTF-8')
        add = Tadmin(nama=form.nama.data,
                     username=form.username.data, password=pass_hash)
        db.session.add(add)
        db.session.commit()
        flash(f'Akun berhasil daftar', 'primary')
        return redirect(url_for('Sadmin.admin'))
    return render_template("admin/daftar_admin.html", form=form)

@Sadmin.route("/admin",  methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('Sadmin.dasboard'))
    form = admin_F()
    if request.method == 'POST':
        cekusername = Tadmin.query.filter_by(
            username=form.username.data).first()
        if cekusername and bcrypt.check_password_hash(cekusername.password, form.password.data):
            login_user(cekusername)
            flash('selamat Datang Kembali', 'warning')
            return redirect(url_for('Sadmin.dasboard'))
        else:
            flash('login gagal, periksa username dan Password!', 'danger')
    return render_template("admin/login_admin.html", form=form)


@Sadmin.route("/logout_admin")
def logout_admin():
    return redirect(url_for('Suser.home'))


@Sadmin.route("/base")
def base3():
    return render_template("admin/base.html")

@Sadmin.route("/dasboard")
def dasboard():
    demografi=len(DataDemog.query.all())
    return render_template("admin/base.html", total_demografi=demografi)

# Wisata
@Sadmin.route("/data-wisata", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data-wisata/<int:page>", methods=['GET', 'POST']) #pagenation
def data_wisata(page):#pagenation
    form = wisatawan_kuliner_F()
    Dataa = Twisata_kuliner.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    wisata = Twisata_kuliner.query.order_by(Twisata_kuliner.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        wisata = Twisata_kuliner.query.filter(Twisata_kuliner.kategori.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_wisata.html", Data=Dataa, form=form, wisata=wisata, tag=tag)
    if form.validate_on_submit():
        filevideo=simpan_video(form.video.data)
        filefoto=simpan_foto(form.gambar.data)
        add = Twisata_kuliner(nama=form.nama.data, lokasi=form.lokasi.data,kategori=form.kategori.data, status=form.status.data,  nama_pemilik=form.nama_pemilik.data,  deskripsi=form.deskripsi.data,  gambar=filefoto, video=filevideo)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_wisata'))
    return render_template("admin/data_wisata.html", Data=Dataa, form=form, wisata=wisata)

@Sadmin.route("/editwisata/<int:ed_id>/update", methods=['GET', 'POST'])
def update_wisata(ed_id):
    e_wisata= Twisata_kuliner.query.get_or_404(ed_id)
    form=ewisatawan_kuliner_F()
    if form.validate_on_submit():
        filevideo=simpan_video(form.video.data)
        filefoto=simpan_foto(form.gambar.data)
        e_wisata.nama=form.nama.data
        e_wisata.lokasi=form.lokasi.data
        e_wisata.kategori=form.kategori.data
        e_wisata.status=form.status.data
        e_wisata.nama_pemilik=form.nama_pemilik.data
        e_wisata.deskripsi=form.deskripsi.data
        e_wisata.gambar=filefoto
        e_wisata.video=filevideo
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_wisata'))
    elif request.method=="GET":
        form.nama.data=e_wisata.nama
        form.lokasi.data=e_wisata.lokasi
        form.kategori.data=e_wisata.kategori
        form.status.data=e_wisata.status
        form.nama_pemilik.data=e_wisata.nama_pemilik
        form.deskripsi.data=e_wisata.deskripsi
        form.gambar.data=e_wisata.gambar
        form.video.data=e_wisata.video
    return render_template('admin/edit_wisata.html', form=form)

@Sadmin.route("/hapuswisata/<id>", methods=['GET', 'POST'])
def hapus_wisata(id):
    data_wisata=Twisata_kuliner.query.get(id)
    db.session.delete(data_wisata)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_wisata'))
# Akhir Wisata

# Prasarana
@Sadmin.route("/data_prasarana", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_prasarana/<int:page>", methods=['GET', 'POST']) #pagenation
def sarana(page):#pagenation
    form = prasarana_F()
    Dataa = Tprasarana.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    prasarana = Tprasarana.query.order_by(Tprasarana.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        prasarana = Tprasarana.query.filter(Tprasarana.kategori.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_sarana.html", Data=Dataa, form=form, prasarana=prasarana, tag=tag)
    if form.validate_on_submit():
        filefoto=simpan_foto(form.foto.data)
        add = Tprasarana(nama=form.nama.data, lokasi=form.lokasi.data, status=form.status.data, tahun_berdiri=form.tahun_berdiri.data, kategori=form.kategori.data, foto=filefoto)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.sarana'))
    return render_template("admin/data_sarana.html", Data=Dataa, form=form, prasarana=prasarana)

@Sadmin.route("/editprasarana/<int:ed_id>/update", methods=['GET', 'POST'])
def update_prasarana(ed_id):
    e_prasarana= Tprasarana.query.get_or_404(ed_id)
    form=eprasarana_F()
    if form.validate_on_submit():
        filefoto=simpan_foto(form.foto.data)
        e_prasarana.nama=form.nama.data
        e_prasarana.lokasi=form.lokasi.data
        e_prasarana.status=form.status.data
        e_prasarana.tahun_berdiri=form.tahun_berdiri.data
        e_prasarana.kategori=form.kategori.data
        e_prasarana.foto=filefoto
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_sarana'))
    elif request.method=="GET":
        form.nama.data=e_prasarana.nama
        form.lokasi.data=e_prasarana.lokasi
        form.status.data=e_prasarana.status
        form.tahun_berdiri.data=e_prasarana.tahun_berdiri
        form.kategori.data=e_prasarana.kategori
        form.foto.data=e_prasarana.foto
    return render_template('admin/edit_prasarana.html', form=form)

@Sadmin.route("/hapusprasarana/<id>", methods=['GET', 'POST'])
def hapus_prasarana(id):
    data_prasarana=Tprasarana.query.get(id)
    db.session.delete(data_prasarana)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_sarana'))
# Akhir Prasarana

# Perangkat Desa
@Sadmin.route("/data_perangkat", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_perangkat/<int:page>", methods=['GET', 'POST']) #pagenation
def perangkat_desa(page):#pagenation
    form = perangkat_desa_F()
    Dataa = Tperangkat_desa.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    perangkat = Tperangkat_desa.query.order_by(Tperangkat_desa.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        perangkat = Tperangkat_desa.query.filter(Tperangkat_desa.kategori.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_sarana.html", Data=Dataa, form=form, perangkat=perangkat, tag=tag)
    if form.validate_on_submit():
        filefoto=simpan_foto(form.gambar.data)
        add = Tperangkat_desa(nama=form.nama.data, jabatan=form.jabatan.data, gambar=filefoto)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.perangkat_desa'))
    return render_template("admin/data_perangkat.html", Data=Dataa, form=form, perangkat=perangkat)

@Sadmin.route("/editperangkat/<int:ed_id>/update", methods=['GET', 'POST'])
def update_perangkat(ed_id):
    e_perangkat= Tperangkat_desa.query.get_or_404(ed_id)
    form=eperangkat_desa_F()
    if form.validate_on_submit():
        filefoto=simpan_foto(form.gambar.data)
        e_perangkat.nama=form.nama.data
        e_perangkat.jabatan=form.jabatan.data
        e_perangkat.gambar=filefoto
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.perangkat_desa'))
    elif request.method=="GET":
        form.nama.data=e_perangkat.nama
        form.jabatan.data=e_perangkat.jabatan
        form.gambar.data=e_perangkat.gambar
    return render_template('admin/edit_perangkat.html', form=form)

@Sadmin.route("/hapusperangkat/<id>", methods=['GET', 'POST'])
def hapus_perangkat(id):
    data_perangkat=Tperangkat_desa.query.get(id)
    db.session.delete(data_perangkat)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.perangkat_desa'))
# Akhir Perangkat Desa

# berita
@Sadmin.route("/kabar_desa", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/kabar_desa/<int:page>", methods=['GET', 'POST']) #pagenation
def data_kabar_desa(page):#pagenation
    form = kabar_desa_F()
    Dataa = Tkabar_desa.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    berita = Tkabar_desa.query.order_by(Tkabar_desa.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        berita = Tkabar_desa.query.filter(Tkabar_desa.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/kabar_desa.html", Data=Dataa, form=form, berita=berita, tag=tag)
    if form.validate_on_submit():
        filefoto=simpan_foto(form.gambar.data)
        filevideo=simpan_video(form.video.data)
        add = Tkabar_desa(judul=form.judul.data, kategori=form.kategori.data, deskripsi=form.deskripsi.data, gambar=filefoto, video=filevideo)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_kabar_desa'))
    return render_template("admin/kabar_desa.html", Data=Dataa, form=form, berita=berita)

@Sadmin.route("/editberita/<int:ed_id>/update", methods=['GET', 'POST'])
def update_berita(ed_id):
    e_berita= Tkabar_desa.query.get_or_404(ed_id)
    form=ekabar_desa_F()
    if form.validate_on_submit():
        filevideo=simpan_video(form.video.data)
        filefoto=simpan_foto(form.gambar.data)
        e_berita.judul=form.judul.data
        e_berita.kategori=form.kategori.data
        e_berita.deskripsi=form.deskripsi.data
        e_berita.gambar=filefoto
        e_berita.video=filevideo
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_kabar_desa'))
    elif request.method=="GET":
        form.judul.data=e_berita.judul
        form.kategori.data=e_berita.kategori
        form.deskripsi.data=e_berita.deskripsi
        form.gambar.data=e_berita.gambar
        form.video.data=e_berita.video
    return render_template('admin/edit_berita.html', form=form)

@Sadmin.route("/hapusberita/<id>", methods=['GET', 'POST'])
def hapus_berita(id):
    berita=Tkabar_desa.query.get(id)
    db.session.delete(berita)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_kabar_desa'))
# Akhir Berita

# Demografi
@Sadmin.route("/data_demografis2", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_demografis2/<int:page>", methods=['GET', 'POST']) #pagenation
def data_demog2(page):#pagenation
    form = DataDemog_F()
    Dataa = DataDemog.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    demografi = DataDemog.query.order_by(DataDemog.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        demografi = DataDemog.query.filter(DataDemog.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_demog.html", Data=Dataa, form=form, demografi=demografi, tag=tag)
    #akhir kode search
    if form.validate_on_submit():
        add = DataDemog(tahun=form.tahun.data, jumlah_l=form.jumlah_l.data,
                        jumlah_p=form.jumlah_p.data,  laju_pertumbuhan=form.laju_pertumbuhan.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_demog2'))
    return render_template("admin/data_demog.html", Data=Dataa, form=form, demografi=demografi)

@Sadmin.route("/hapusdemografi/<id>", methods=['GET', 'POST'])
def hapus_kategori(id):
    demografi=DataDemog.query.get(id)
    db.session.delete(demografi)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_demog2'))

@Sadmin.route("/editdemo/<int:ed_id>/update", methods=['GET', 'POST'])
def update_demo(ed_id):
    e_demografi= DataDemog.query.get_or_404(ed_id)
    form=edit_datademog_F()
    if form.validate_on_submit():
        e_demografi.tahun=form.tahun.data
        e_demografi.jumlah_l=form.jumlah_l.data
        e_demografi.jumlah_p=form.jumlah_p.data
        e_demografi.laju_pertumbuhan=form.laju_pertumbuhan.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_demog2'))
    elif request.method=="GET":
        form.tahun.data=e_demografi.tahun
        form.jumlah_l.data=e_demografi.jumlah_l
        form.jumlah_p.data=e_demografi.jumlah_p
        form.laju_pertumbuhan.data=e_demografi.laju_pertumbuhan
    return render_template('admin/edit_demografi.html', form=form)
# Akhir Demografi

# Pendidikan
@Sadmin.route("/data_pendidikan", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_pendidikan/<int:page>", methods=['GET', 'POST']) #pagenation
def data_pendidikan(page):#pagenation
    form = pendidikan_F()
    Dataa = Tpendidikan.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    pendidikan = Tpendidikan.query.order_by(Tpendidikan.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        pendidikan = Tpendidikan.query.filter(Tpendidikan.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_pendidikan.html", Data=Dataa, form=form, pendidikan=pendidikan, tag=tag)
    #akhir kode search
    if form.validate_on_submit():
        add = Tpendidikan(tahun=form.tahun.data, tdk_sd=form.tdk_sd.data,
                        tamat_sd=form.tamat_sd.data, tamat_smp=form.tamat_smp.data, tamat_sma=form.tamat_sma.data, tamat_s1=form.tamat_s1.data, tamat_s2=form.tamat_s2.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_pendidikan'))
    return render_template("admin/data_pendidikan.html", Data=Dataa, form=form, pendidikan=pendidikan)

@Sadmin.route("/editpendidikan/<int:ed_id>/update", methods=['GET', 'POST'])
def update_pendidikan(ed_id):
    e_pendidikan= Tpendidikan.query.get_or_404(ed_id)
    form=ependidikan_F()
    if form.validate_on_submit():
        e_pendidikan.tahun=form.tahun.data
        e_pendidikan.tdk_sd=form.tdk_sd.data
        e_pendidikan.tamat_sd=form.tamat_sd.data
        e_pendidikan.tamat_smp=form.tamat_smp.data
        e_pendidikan.tamat_sma=form.tamat_sma.data
        e_pendidikan.tamat_s1=form.tamat_s1.data
        e_pendidikan.tamat_s2=form.tamat_s2.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_pendidikan'))
    elif request.method=="GET":
        form.tahun.data=e_pendidikan.tahun
        form.tdk_sd.data=e_pendidikan.tdk_sd
        form.tamat_sd.data=e_pendidikan.tamat_sd
        form.tamat_smp.data=e_pendidikan.tamat_smp
        form.tamat_sma.data=e_pendidikan.tamat_sma
        form.tamat_s1.data=e_pendidikan.tamat_s1
        form.tamat_s2.data=e_pendidikan.tamat_s2
    return render_template('admin/edit_pendidikan.html', form=form)

@Sadmin.route("/hapuspendidikan/<id>", methods=['GET', 'POST'])
def hapus_pendidikan(id):
    pendidikan=Tpendidikan.query.get(id)
    db.session.delete(pendidikan)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_pendidikan'))
# Akhir Pendidikan

# Penduduk
@Sadmin.route("/data_penduduk", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_penduduk/<int:page>", methods=['GET', 'POST']) #pagenation
def dt_penduduk(page):#pagenation
    form = penduduk_F()
    Dataa = Tpenduduk.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    penduduk = Tpenduduk.query.order_by(Tpenduduk.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        penduduk = Tpenduduk.query.filter(Tpenduduk.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_penduduk.html", Data=Dataa, form=form, penduduk=penduduk, tag=tag)
    #akhir kode search
    if form.validate_on_submit():
        add = Tpenduduk(no_ktp=form.no_ktp.data ,no_kk=form.no_kk.data, nama=form.nama.data,
                        tgl_lahir=form.tgl_lahir.data, j_kelamin=form.j_kelamin.data, agama=form.agama.data, pendidikan=form.pendidikan.data, pekerjaan=form.pekerjaan.data, alamat=form.alamat.data, RT=form.RT.data, RW=form.RW.data, s_nikah=form.s_nikah.data, kewarganegaraan=form.kewarganegaraan.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.dt_penduduk'))
    return render_template("admin/data_penduduk.html", Data=Dataa, form=form, penduduk=penduduk)

@Sadmin.route("/editpenduduk/<int:ed_id>/update", methods=['GET', 'POST'])
def update_penduduk(ed_id):
    e_penduduk= Tpenduduk.query.get_or_404(ed_id)
    form=ependuduk_F()
    if form.validate_on_submit():
        e_penduduk.no_ktp=form.no_ktp.data
        e_penduduk.no_kk=form.no_kk.data
        e_penduduk.nama=form.nama.data
        e_penduduk.tgl_lahir=form.tgl_lahir.data
        e_penduduk.j_kelamin=form.j_kelamin.data
        e_penduduk.agama=form.agama.data
        e_penduduk.pendidikan=form.pendidikan.data
        e_penduduk.pekerjaan=form.pekerjaan.data
        e_penduduk.alamat=form.alamat.data
        e_penduduk.RT=form.RT.data
        e_penduduk.RW=form.RW.data
        e_penduduk.s_nikah=form.s_nikah.data
        e_penduduk.kewarganegaraan=form.kewarganegaraan.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.dt_penduduk'))
    elif request.method=="GET":
        form.no_ktp.data=e_penduduk.no_ktp
        form.no_kk.data=e_penduduk.no_kk
        form.nama.data=e_penduduk.nama
        form.tgl_lahir.data=e_penduduk.tgl_lahir
        form.j_kelamin.data=e_penduduk.j_kelamin
        form.agama.data=e_penduduk.agama
        form.pendidikan.data=e_penduduk.pendidikan
        form.pekerjaan.data=e_penduduk.pekerjaan
        form.alamat.data=e_penduduk.alamat
        form.RT.data=e_penduduk.RT
        form.RW.data=e_penduduk.RW
        form.s_nikah.data=e_penduduk.s_nikah
        form.kewarganegaraan.data=e_penduduk.kewarganegaraan
    return render_template('admin/edit_penduduk.html', form=form)

@Sadmin.route("/hapuspenduduk/<id>", methods=['GET', 'POST'])
def hapus_penduduk(id):
    penduduk=Tpenduduk.query.get(id)
    db.session.delete(penduduk)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.dt_penduduk'))
# Akhir Penduduk




# Putus Sekolah
@Sadmin.route("/data_putus_sklh", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_putus_sklh/<int:page>", methods=['GET', 'POST']) #pagenation
def data_pts_sekolah(page):#pagenation
    form = putus_sekolah_F()
    Dataa = Tputus_sekolah.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    putus_sekolah = Tputus_sekolah.query.order_by(Tputus_sekolah.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        putus_sekolah = Tputus_sekolah.query.filter(Tputus_sekolah.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_putus_sekolah.html", Data=Dataa, form=form, putus_sekolah=putus_sekolah, tag=tag)
    #akhir kode search
    if form.validate_on_submit():
        add = Tputus_sekolah(tahun=form.tahun.data, sd=form.sd.data, smp=form.smp.data, sma=form.sma.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_pts_sekolah'))
    return render_template("admin/data_putus_sekolah.html", Data=Dataa, form=form, putus_sekolah=putus_sekolah)

@Sadmin.route("/editputus_sekolah/<int:ed_id>/update", methods=['GET', 'POST'])
def update_putus_sklh(ed_id):
    e_putus_sekolah= Tputus_sekolah.query.get_or_404(ed_id)
    form=eputus_sekolah_F()
    if form.validate_on_submit():
        e_putus_sekolah.tahun=form.tahun.data
        e_putus_sekolah.sd=form.sd.data
        e_putus_sekolah.smp=form.smp.data
        e_putus_sekolah.sma=form.sma.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.data_pts_sekolah'))
    elif request.method=="GET":
        form.tahun.data=e_putus_sekolah.tahun
        form.sd.data=e_putus_sekolah.sd
        form.smp.data=e_putus_sekolah.smp
        form.sma.data=e_putus_sekolah.sma
    return render_template('admin/edit_putus_sekolah.html', form=form)

@Sadmin.route("/hapusputus_sekolah/<id>", methods=['GET', 'POST'])
def hapus_putus_sekolaj(id):
    putus_sekolah=Tputus_sekolah.query.get(id)
    db.session.delete(putus_sekolah)
    db.session.commit()
    flash('Data Berhasil Di hapus','danger')
    return redirect(url_for('Sadmin.data_pts_sekolah'))
# Akhir Putus Sekolah

# Surat
@Sadmin.route("/profil2", methods=['GET', 'POST'])
def profil2():
    Data = Tprofil.query.all()
    return render_template("admin/profil.html", profil=Data)

# edit profil yg benar
@Sadmin.route("/editprofil/<int:ed_id>/update", methods=['GET', 'POST'])
def update_profil(ed_id):
    e_profil=Tprofil.query.get_or_404(ed_id)
    form=eprofil_F()
    if form.validate_on_submit():
        e_profil.nama_desa=form.nama_desa.data
        e_profil.visi=form.visi.data
        e_profil.misi=form.misi.data
        e_profil.alamat=form.alamat.data
        e_profil.sejerah=form.sejarah.data
        e_profil.peraturan=form.peraturan.data
        e_profil.geografis=form.geografis.data
        e_profil.kontak=form.kontak.data
        db.session.commit()
        flash('Data Berhasil Di ubah','info')
        return redirect(url_for('Sadmin.profil2'))
    elif request.method=="GET":
        form.nama_desa.data=e_profil.nama_desa
        form.visi.data=e_profil.visi
        form.misi.data=e_profil.misi
        form.alamat.data=e_profil.alamat
        form.sejarah.data=e_profil.sejarah
        form.peraturan.data=e_profil.peraturan
        form.geografis.data=e_profil.geografis
        form.kontak.data=e_profil.kontak
    return render_template('admin/edit_profil.html', form=form)



# Surat
@Sadmin.route("/data_surat", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Sadmin.route("/data_surat/<int:page>", methods=['GET', 'POST']) #pagenation
def data_surat(page):#pagenation
    form = surat_F()
    Dataa = Tsurat_ket.query.all()
    #return render_template("data_demog2.html", Data=Dataa)
    page = page #pagenation2
    pages = 10 #pagenation3
    surat = Tsurat_ket.query.order_by(Tsurat_ket.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    form.nik.choices = [(str(tpenduduk.id), tpenduduk.nama ) for tpenduduk in Tpenduduk.query.all()]
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        surat = Tsurat_ket.query.filter(Tsurat_ket.nama.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_surat.html", Data=Dataa, form=form, surat=surat, tag=tag)
    #akhir kode search
    if form.validate_on_submit():
        add = Tsurat_ket(no_surat=form.no_surat.data, jenis_surat=form.jenis_surat.data, keperluan=form.keperluan.data, penduduk_id=form.nik.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_surat'))
    return render_template("admin/data_surat.html", Data=Dataa, form=form, surat=surat)


@Sadmin.route("/cetak_menikah/<int:ed_id>/update", methods=['GET', 'POST'])
def cetaknikah(ed_id):
    d_surat= Tsurat_ket.query.get_or_404(ed_id)
    camat= Tperangkat_desa.query.filter( Tperangkat_desa.jabatan.like("KEPALA DESA TEMBAL"))
    ambil_camat = Tperangkat_desa.query.filter_by(jabatan="CAMAT BACAN SELATAN").all()
    for camat in ambil_camat:
        c = camat

    ambil_kades = Tperangkat_desa.query.filter_by(jabatan="KEPALA DESA TEMBAL").all()
    for kades in ambil_kades:
        d = kades

    return render_template('admin/surat/surat_b_menikah.html', d_surat=d_surat, camat=c, kades=d)

@Sadmin.route("/cetak_domisili/<int:ed_id>/update", methods=['GET', 'POST'])
def cetakdomisili(ed_id):
    d_surat= Tsurat_ket.query.get_or_404(ed_id)
    camat= Tperangkat_desa.query.filter( Tperangkat_desa.jabatan.like("KEPALA DESA TEMBAL"))
    ambil_camat = Tperangkat_desa.query.filter_by(jabatan="CAMAT BACAN SELATAN").all()
    for camat in ambil_camat:
        c = camat

    ambil_kades = Tperangkat_desa.query.filter_by(jabatan="KEPALA DESA TEMBAL").all()
    for kades in ambil_kades:
        d = kades

    return render_template('admin/surat/surat_domisili.html', d_surat=d_surat, camat=c, kades=d)

@Sadmin.route("/cetak_sbm/<int:ed_id>/update", methods=['GET', 'POST'])
def cetaksbm(ed_id):
    d_surat= Tsurat_ket.query.get_or_404(ed_id)
    camat= Tperangkat_desa.query.filter( Tperangkat_desa.jabatan.like("KEPALA DESA TEMBAL"))
    ambil_camat = Tperangkat_desa.query.filter_by(jabatan="CAMAT BACAN SELATAN").all()
    for camat in ambil_camat:
        c = camat

    ambil_kades = Tperangkat_desa.query.filter_by(jabatan="KEPALA DESA TEMBAL").all()
    for kades in ambil_kades:
        d = kades

    return render_template('admin/surat/surat_kbm.html', d_surat=d_surat, camat=c, kades=d)



# # edit profil yg benar
# @Sadmin.route("/editprofil/<int:ed_id>/update", methods=['GET', 'POST'])
# def update_profil(ed_id):
#     e_profil=Tprofil.query.get_or_404(ed_id)
#     form=eprofil_F()
#     if form.validate_on_submit():
#         e_profil.nama_desa=form.nama_desa.data
#         e_profil.visi=form.visi.data
#         e_profil.misi=form.misi.data
#         e_profil.alamat=form.alamat.data
#         e_profil.sejerah=form.sejarah.data
#         e_profil.peraturan=form.peraturan.data
#         e_profil.geografis=form.geografis.data
#         e_profil.kontak=form.kontak.data
#         db.session.commit()
#         flash('Data Berhasil Di ubah','info')
#         return redirect(url_for('Sadmin.profil2'))
#     elif request.method=="GET":
#         form.nama_desa.data=e_profil.nama_desa
#         form.visi.data=e_profil.visi
#         form.misi.data=e_profil.misi
#         form.alamat.data=e_profil.alamat
#         form.sejarah.data=e_profil.sejarah
#         form.peraturan.data=e_profil.peraturan
#         form.geografis.data=e_profil.geografis
#         form.kontak.data=e_profil.kontak
#     return render_template('admin/edit_profil.html', form=form)

@Sadmin.route("/isi_data_profil", methods=['GET', 'POST'])
def isi_data_profil():
    form = profil_F()
    if form.validate_on_submit():
        add = Tprofil(nama_desa=form.nama_desa.data, visi=form.visi.data, misi=form.misi.data, alamat=form.alamat.data, sejarah=form.sejarah.data, peraturan=form.peraturan.data, geografis=form.geografis.data, kontak=form.kontak.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.profil2'))
    return render_template("edit_profil.html", form=form)
# Surat




























