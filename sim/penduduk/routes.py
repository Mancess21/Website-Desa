from pydoc import describe
from tkinter.tix import Form
from sim import db, bcrypt
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
# from sim.admin.routes import data_pts_sekolah

from sim.penduduk.forms import login, profil_F, DataDemog_F, penduduk_F, surat_F, admin_F, kabar_desa_F, pendidikan_F, prasarana_F, putus_sekolah_F, wisatawan_kuliner_F
from sim.models import Tpenduduk, Tperangkat_desa, Tprofil, DataDemog, Tsurat_ket, Tadmin, Tpendidikan, Tprasarana, Tputus_sekolah, Tkabar_desa, Twisata_kuliner


Suser = Blueprint('Suser', __name__)


@Suser.route("/", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("//<int:page>", methods=['GET', 'POST'])
def home(page):
    page=page
    pages=10
    dataprofil= Tprofil.query.all()

    j_kuliner = len(Twisata_kuliner.query.all())
    j_prasarana = len(Tprasarana.query.all())
    j_penduduk = len(Tpenduduk.query.all())

    data_demografi = DataDemog.query.all()
    for laju in data_demografi:
        laju_pertumbuhan = laju
    
    data_pendidik = Tpendidikan.query.all()
    for pendidik in data_pendidik:
        data_pendidikan = pendidik
    
    data_putus = Tputus_sekolah.query.all()
    for putus in data_putus:
        data_pts_sekolah = putus
    

    # datasekolah = Tputus_sekolah.query.order_by(Tputus_sekolah.id.desc()).paginate(page, pages, error_out=False)
    datakuliner = Twisata_kuliner.query.order_by(Twisata_kuliner.id.desc()).paginate(page, pages, error_out=False)
    datakabar = Tkabar_desa.query.order_by(Tkabar_desa.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/index.html",dataprofil=dataprofil, datakuliner=datakuliner,  datakabar=datakabar, j_kuliner=j_kuliner,  pendidikan=putus, demog2=laju, pendidik2=pendidik, j_prasarana= j_prasarana, j_penduduk=j_penduduk, data_demografi=data_demografi)


@Suser.route("/profil", methods=['GET', 'POST'])
def profil():
    dataprofil = Tprofil.query.all()
    return render_template("user/profil.html", dataprofil=dataprofil)


@Suser.route("/aperatur", methods=['GET', 'POST'])
def aperatur():
    dataaperatur = Tperangkat_desa.query.all()
    return render_template("user/Aperatur_desa.html", dataaperatur=dataaperatur)


@Suser.route("/userwisata", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/userwisata/<int:page>", methods=['GET', 'POST'])
def userwisata(page):
    page=page
    pages=20
    datakuliner = Twisata_kuliner.query.order_by(Twisata_kuliner.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/user_wisata.html",  datakuliner=datakuliner,)


@Suser.route("/usersekolah", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/usersekolah/<int:page>", methods=['GET', 'POST'])
def usersekolah(page):
    page=page
    pages=20
    datasekolah = Tputus_sekolah.query.order_by(Tputus_sekolah.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/user_sekolah.html",  datasekolah=datasekolah,)


@Suser.route("/userstatic", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/userstatic/<int:page>", methods=['GET', 'POST'])
def userstatic(page):
    page=page
    pages=10
    datapendidikan = Tpendidikan.query.order_by(Tpendidikan.id.desc()).paginate(page, pages, error_out=False)
    dataputus_sekolah = Tputus_sekolah.query.order_by(Tputus_sekolah.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/user_wisata.html",  datapendidikan=datapendidikan, dataputus_sekolah=dataputus_sekolah)


@Suser.route("/visimisi", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/visimisi/<int:page>", methods=['GET', 'POST'])
def visimisi(page):
    page=page
    pages=10
    dataprofil= Tprofil.query.all()
    # dataprofil = Tprofil.query.order_by(Tprofil.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/visimisi.html", dataprofil=dataprofil)




@Suser.route("/fasilitas_desa", methods=['GET', 'POST'])
def fasilitasdesa():
    datafasilitas = Tprasarana.query.all()
    return render_template("user/fasilitas.html", datafasilitas=datafasilitas)


@Suser.route("/peta_desa", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/peta_desa/<int:page>", methods=['GET', 'POST'])
def petadesa(page):
    page=page
    pages=10
    datapeta= Tprofil.query.all()
    # datapeta = Tprofil.query.order_by(Tprofil.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/peta.html", datapeta=datapeta)


@Suser.route("/sejarah", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/sejarah/<int:page>", methods=['GET', 'POST'])
def sejarah(page):
    page=page
    pages=10
    dataprofil= Tprofil.query.all()
    # dataprofil = Tprofil.query.order_by(Tprofil.id.desc()).paginate(page, pages, error_out=False)
    return render_template("user/sejarah.html", dataprofil=dataprofil)


@Suser.route("/berita", methods=['GET', 'POST'])
def berita():
    databerita = Tkabar_desa.query.all()
    return render_template("user/berita.html", databerita=databerita)

@Suser.route("/wisata", methods=['GET', 'POST'])
def wisata():
    datawisata = Twisata_kuliner.query.all()
    return render_template("user/wisata.html", datawisata=datawisata)


@Suser.route("/hubungi", methods=['GET', 'POST'])
def hubungi():
    # form = Tprofil.query.all()
    return render_template("user/hubungi.html")


@Suser.route("/detailwisata/<int:ed_id>/update", methods=['GET', 'POST'])
def detail_wisata(ed_id):
    d_wisata= Twisata_kuliner.query.get_or_404(ed_id)
    return render_template('user/detail_wisata.html', d_wisata=d_wisata)


@Suser.route("/detailberita/<int:ed_id>/update", methods=['GET', 'POST'])
def detail_berita(ed_id):
    d_berita= Tkabar_desa.query.get_or_404(ed_id)
    return render_template('user/detail_berita.html', d_berita=d_berita)


@Suser.route("/data_statistik", methods=['GET', 'POST'], defaults={"page": 3})#pagenation1
@Suser.route("/data_statistik/<int:page>", methods=['GET', 'POST']) #pagenation
def datastatistik(page):#pagenation
    Dataa = DataDemog.query.all()
    Dataa = Tpendidikan.query.all()
    Dataa = Tputus_sekolah.query.all()
    page = page #pagenation2
    pages = 10 #pagenation3
    demografi = DataDemog.query.order_by(DataDemog.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    pendidikan = Tpendidikan.query.order_by(Tpendidikan.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    ptssklh = Tputus_sekolah.query.order_by(Tputus_sekolah.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        demografi = DataDemog.query.filter(DataDemog.tahun.like(search)).paginate(page, pages, error_out=False)
        pendidikan = Tpendidikan.query.filter(Tpendidikan.tahun.like(search)).paginate(page, pages, error_out=False)
        ptssklh = Tputus_sekolah.query.filter(Tputus_sekolah.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_demog.html", Data=Dataa, form=Form, demografi=demografi, pendidikan=pendidikan, ptssklh=ptssklh, tag=tag)
        return render_template("admin/data_pendidikan.html", Data=Dataa, form=Form, demografi=demografi, pendidikan=pendidikan, ptssklh=ptssklh, tag=tag)
        return render_template("admin/data_putus_sekolah.html", Data=Dataa, form=Form, demografi=demografi, pendidikan=pendidikan, ptssklh=ptssklh, tag=tag)
    #akhir kode search
    return render_template("user/Data_statistik.html", Data=Dataa, demografi=demografi, pendidikan=pendidikan, ptssklh=ptssklh)


@Suser.route("/user_demo", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Suser.route("/data_demo/<int:page>", methods=['GET', 'POST']) #pagenation
def userdemo(page):#pagenation
    Dataa = DataDemog.query.all()
    page = page #pagenation2
    pages = 10 #pagenation3
    demografi = DataDemog.query.order_by(DataDemog.id.asc()).paginate(page, pages, error_out=False) #pagenation4
    #kode search
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        demografi = DataDemog.query.filter(DataDemog.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/data_demog.html", Data=Dataa, form=Form, demografi=demografi, tag=tag)
    #akhir kode search
    return render_template("user/user_demo.html", Data=Dataa, demografi=demografi)


@Suser.route("/user_pendidikan", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Suser.route("/user_pendidikan/<int:page>", methods=['GET', 'POST']) #pagenation
def userpendidikan(page):#pagenation
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
        return render_template("admin/data_pendidikan.html", Data=Dataa, form=Form, pendidikan=pendidikan, tag=tag)
    #akhir kode search
    return render_template("user/user_pendidikan.html", Data=Dataa, pendidikan=pendidikan)


@Suser.route("/user_fasilitas", methods=['GET', 'POST'], defaults={"page": 1})#pagenation1
@Suser.route("/user_fasilitas/<int:page>", methods=['GET', 'POST']) #pagenation
def usersarana(page):#pagenation
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
        return render_template("admin/data_sarana.html", Data=Dataa, prasarana=prasarana, tag=tag)
    return render_template("user/user_fasilitas.html", Data=Dataa, prasarana=prasarana)






























@Suser.route("/data_demografis", methods=['GET', 'POST'])
def data_demog():
    Dataa = DataDemog.query.all()
    return render_template("data_demog.html", Data=Dataa)


@Suser.route("/ketrangan", methods=['GET', 'POST'])
def ketrangan():
    if not current_user.is_authenticated:
        return redirect(url_for('Suser.user'))
    Data = Tsurat_ket.query.filter_by(penduduk_id=current_user.id)
    form = surat_F()
    if request.method == 'POST':
        # tambah data pengaduan
        add = Tsurat_ket(kategori=form.kategori.data,
                         keterangan=form.keterangan.data, penduduk=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasisl ditambahkan', 'warning')
        return redirect(url_for('Suser.ketrangan'))
    return render_template("surat_ket.html", form=form, Data=Data)


@Suser.route("/registrasi",  methods=['GET', 'POST'])
def daftar2():
    form = penduduk_F()
    if request.method == 'POST':
        pass_hash = bcrypt.generate_password_hash(
            form.password.data).decode('UTF-8')
        data = Tpenduduk(nik=form.nik.data, nama=form.nama.data, tgl_lahir=form.tgl_lahir.data,
                         email=form.email.data, password=pass_hash, alamat=form.alamat.data, tlp=form.tlp.data)
        db.session.add(data)
        db.session.commit()
        flash('Akun berhasil daftar', 'primary')
        return redirect(url_for('Suser.user'))
    return render_template("daftar.html", form=form)


@Suser.route("/user",  methods=['GET', 'POST'])
def user():
    if current_user.is_authenticated:
        return redirect(url_for('Suser.home'))
    form = login()
    if request.method == 'POST':
        ceknik = Tpenduduk.query.filter_by(nik=form.username.data).first()
        if ceknik and bcrypt.check_password_hash(ceknik.password, form.password.data):
            login_user(ceknik)
            flash('selamat Datang Kembali', 'warning')
            return redirect(url_for('Suser.home'))
        else:
            flash('login gagal, periksa username dan Password!', 'danger')
    return render_template("login_user.html", form=form)


@Suser.route("/editpengaduan", methods=['GET', 'POST'])
@login_required
def editpengaduan():
    if request.method == 'POST':
        m_data = Tsurat_ket.query.get(request.form.get('id'))
        m_data.kategori = request.form['kategori']
        m_data.keterangan = request.form['keterangan']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('Suser.ketrangan'))


@Suser.route("/hapus_A/<id>", methods=['GET', 'POST'])
@login_required
def hapus_A(id):
    my = Tsurat_ket.query.get(id)
    db.session.delete(my)
    db.session.commit()
    flash('Data berhasisl dihapus', 'warning')
    return redirect(url_for('Suser.ketrangan'))


@Suser.route("/logout_admin")
def logout_admin():
    logout_user()
    return redirect(url_for('Suser.home'))


@Suser.route("/prasarana")
def prasarana():
    return render_template('Suser.prasarana')


@Suser.route("/wisata_kuliner", methods=['GET', 'POST'])
def kuliner():
    if not current_user.is_authenticated:
        return redirect(url_for('Suser.user'))
    Data = Twisata_kuliner.query.filter_by(penduduk_id=current_user.id)
    form = wisatawan_kuliner_F()
    if request.method == 'POST':
        # tambah data pengaduan
        add = Twisata_kuliner(nama=form.nama.data, lokasi=form.lokasi.data, kategori=form.kategori.data,
                              status=form.status.data, nama_pemilik=form.nama_pemilik.data, descripsi=form.descripsi.data, gambar=form.gamabar.data, penduduk=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasisl ditambahkan', 'warning')
        return redirect(url_for('Suser.ketrangan'))
    return render_template("surat_ket.html", form=form, Data=Data)

@Suser.route("/wsta_kuliner", methods=['GET', 'POST'], defaults={"page":1})
@Suser.route("/wsta_kuliner/<int:page>", methods=['GET', 'POST'])
def wis_kuliner(page):
    page=page
    pages=4
    dt_kuliner=Twisata_kuliner.query.all()
    datakuliner = Twisata_kuliner.query.order_by(Twisata_kuliner.id.desc()).paginate(page, pages, error_out=False)
    return render_template("home.html", dt_kuliner=dt_kuliner, datakuliner=datakuliner)



# @Suser.route("/visi_misi", methods=['GET', 'POST'])
# def visimisi():
#     form = Tprofil.query.all()
#     return render_template("visi_misi.html", form=form)


# @Suser.route("/sejarah", methods=['GET', 'POST'])
# def sejarah():
#     form = Tprofil.query.all()
#     return render_template("sejarah.html", form=form)



