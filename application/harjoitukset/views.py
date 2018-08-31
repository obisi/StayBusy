from application import app, db, login_manager, login_required
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.juoksuharjoitukset.models import Juoksu
from application.juoksuharjoitukset.forms import JuoksuForm
from application.kuntosaliharjoitukset.models import Salikerta
from application.kuntosaliharjoitukset.forms import SaliForm
from application.kuntosaliharjoitukset.forms import Salikerta_LiikeForm
from application.kuntosaliharjoitukset.models import Salikerta_liike
from application.kuntosaliliikkeet.models import Saliliike
from application.kuntosaliliikkeet.forms import SaliliikeForm
from application.harjoitukset.forms import Pvmhaku_Form
from flask_login import current_user
from application.models import juoksu_print, sali_print, salikerta_liike_print, sali_print_admin, juoksu_print_admin

# erikseen datetime ja datetime datetime koska ilmeisesti eri asia
from datetime import datetime as dt
import datetime


# Listaa kaikki juoksut adminille, tai kaikki käyttäjän juoksut käyttäjälle

@app.route("/harjoitukset/", methods=["GET"])
@login_required()
def harjoitukset_index():
    if current_user.role=="ADMIN":
        juoksut = Juoksu.query.all()
        salit = Salikerta.query.all()
        jt = []
        for j in juoksut:
            jt.append(juoksu_print_admin(j.id, j.pvm, j.aika, j.aika, Juoksu.kenen_juoksu(j.id)[0]))
        st = []
        for s in salit:
            st.append(sali_print_admin(s.id, s.pvm, s.aika, Salikerta.kenen_sali(s.id)[0]))
    else:
        juoksut = Juoksu.kaikki_juoksut(current_user.id)
        salit = Salikerta.kaikki_salikerrat(current_user.id)
        jt = []
        for j in juoksut:
            jt.append(juoksu_print(j['id'], j['pvm'], j['aika'], j['matka']))
        st = []
        for s in salit:
            st.append(sali_print(s['id'], s['pvm'], s['aika']))

    
    return render_template("/harjoitukset/list.html", juoksut = jt, salit = st)


# Luo päivämäärähakuformin
@app.route("/harjoitukset/etsi_pvm/", methods=["GET"])
@login_required()
def pvmhaku_form():
    return render_template("harjoitukset/etsi_pvm.html", form=Pvmhaku_Form())

# Hakee päivämäärällä tietokannasta harjoitukset kahden päivämäärän välillä. Adminille kaikki, käyttäjälle vain omansa
@app.route("/harjoitukset/etsi_pvm/", methods=["POST"])
@login_required()
def pvmhaku():
    form = Pvmhaku_Form(request.form)
    pvmEka = form.pvmEka.data
    pvmToka = form.pvmToka.data
    if current_user.role=="ADMIN":
        juoksut, salit = User.kaikki_harjoitukset_pvm_admin(pvmEka, pvmToka)
        jt = []
        for j in juoksut:
            jt.append(juoksu_print_admin(j['id'], j['pvm'], str(j['aika'])[:-7], j['matka'], Juoksu.kenen_juoksu(j['id'])[0]))
        st = []
        for s in salit:
            st.append(sali_print_admin(s['id'], s['pvm'], str(s['aika'])[:-7], Salikerta.kenen_sali(s['id'])[0]))
    else:
        juoksut, salit = User.kaikki_harjoitukset_pvm(current_user.id, pvmEka, pvmToka)
        jt = []
        for j in juoksut:
            jt.append(juoksu_print(j['id'], j['pvm'], str(j['aika'])[:-7], j['matka']))
        st = []
        for s in salit:
            st.append(sali_print(s['id'], s['pvm'], str(s['aika'])[:-7]))
    return render_template("harjoitukset/etsi_pvm.html", form=form, juoksut=jt, salit=st)


# Juoksuille toiminnallisuudet

# Poistaa juoksun tietokannasta
@app.route("/juoksuharjoitukset/<juoksu_id>/delete", methods=["POST"])
@login_required()
def juoksu_delete(juoksu_id):
    j = Juoksu.query.get(juoksu_id)

    db.session.delete(j)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

# Näyttää yhden juoksun tiedot, sekä laskee sille coopermatkan ja maratonajan
@app.route("/juoksuharjoitukset/<juoksu_id>/single", methods=["GET"])
@login_required()
def juoksu_single(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    uj = juoksu_print(j.id, j.pvm, j.aika, j.matka)

    aika_s = int(j.aika.hour * 3600 + j.aika.minute * 60 + j.aika.second)
    kmh = round((float(j.matka) / aika_s) * 3600, 2)
    cooper = round(kmh * 0.2, 2)
    maraton = round(42.195 / kmh, 2)
    m_aika = str(datetime.timedelta(hours=maraton))
    return render_template("juoksuharjoitukset/single.html", juoksu = uj, kmh = str(kmh) + " km/h",
     cooper = str(cooper) + " km", m_aika = m_aika)

# Päivitysformin luominen juoksulle
@app.route("/juoksuharjoitukset/<juoksu_id>/", methods=["GET"])
@login_required()
def juoksu_updateform(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    form = JuoksuForm(obj=j)
    return render_template("juoksuharjoitukset/edit.html", j=j, form = form)

# Juoksun tietojen editointi
@app.route("/juoksuharjoitukset/<juoksu_id>/", methods=["POST"])
@login_required()
def juoksu_edit(juoksu_id):
    form = JuoksuForm(request.form)
    j = Juoksu.query.get(juoksu_id)

    if not form.validate():
        return render_template("juoksuharjoitukset/edit.html", j=j, form = form)

    j.pvm = form.pvm.data
    j.matka = form.matka.data
    j.aika = form.aika.data

    db.session().commit()
    uj = juoksu_print(j.id, j.pvm, j.aika, j.matka)

    aika_s = int(j.aika.hour * 3600 + j.aika.minute * 60 + j.aika.second)
    kmh = round((float(j.matka) / aika_s) * 3600, 2)
    cooper = round(kmh * 0.2, 2)
    maraton = round(42.195 / kmh, 2)
    m_aika = str(datetime.timedelta(hours=maraton))
    return render_template("juoksuharjoitukset/single.html", juoksu = uj, kmh = str(kmh) + " km/h",
     cooper = str(cooper) + " km", m_aika = m_aika)


# Uuden juoksun formin luominen
@app.route("/juoksuharjoitukset/new/")
@login_required(role="USER")
def juoksut_form():
    form = JuoksuForm(pvm = dt.today().date())
    return render_template("juoksuharjoitukset/new.html", form = form)

# Uuden juoksun luominen tietokantaan
@app.route("/juoksuharjoitukset/", methods=["POST"])
@login_required(role="USER")
def juoksut_create():
    form = JuoksuForm(request.form)
    
    if not form.validate():
        return render_template("juoksuharjoitukset/new.html", form = form)
    j = Juoksu(form.pvm.data, form.matka.data, form.aika.data)
    j.account_id = current_user.id

    db.session().add(j)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

# Saliharjoituksille toiminnallisuudet

# Poistaa yksittäisen saliharjoituksen tietokannasta
@app.route("/kuntosaliharjoitukset/<sali_id>/delete", methods=["POST"])
@login_required()
def sali_delete(sali_id):
    s = Salikerta.query.get(sali_id)

    db.session.delete(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

# Näyttää yksittäisen saliharjoituksen ja siihen liittyvät liikkeet liitostaulusta
@app.route("/kuntosaliharjoitukset/<sali_id>/single", methods=["GET"])
@login_required()
def sali_single(sali_id):
    s = Salikerta.query.get(sali_id)
    us = sali_print(s.id, s.pvm, s.aika)
    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(s.id)
    return render_template("kuntosaliharjoitukset/single.html", sali = us, sk_liikkeet = liikkeet)

# päivitysformi saliharjoitukselle
@app.route("/kuntosaliharjoitukset/<sali_id>/", methods=["GET"])
@login_required()
def sali_updateform(sali_id):
    sali = Salikerta.query.get(sali_id)
    form = SaliForm(obj=sali)
    return render_template("kuntosaliharjoitukset/edit.html", sali=sali, form = form)

# saliharjoituksen päivitys, joka siirtyy lopuksi liitostaulun muokkaukseen
@app.route("/kuntosaliharjoitukset/<sali_id>/", methods=["POST"])
@login_required()
def sali_edit(sali_id):
    form = SaliForm(request.form)
    sali = Salikerta.query.get(sali_id)

    if not form.validate():
        return render_template("kuntosaliharjoitukset/edit.html", sali=sali, form = form)

    sali.pvm = form.pvm.data
    sali.aika = form.aika.data
    db.session().commit()
    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(sali.id)

    form = Salikerta_LiikeForm()
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()

    return render_template("salikerta_liike/new.html", sk_liikkeet = liikkeet, 
        sali_id = sali.id, form = form)

# uuden saliharjoituksen luontiformi
@app.route("/kuntosaliharjoitukset/new/", methods=["GET"])
@login_required(role="USER")
def sali_form():
    form = SaliForm(pvm = dt.today().date())
    return render_template("kuntosaliharjoitukset/new.html", form = form)

# uuden saliharjoituksen luominen
@app.route("/kuntosaliharjoitukset/", methods=["POST"])
@login_required(role="USER")
def sali_create():
    form = SaliForm(request.form)
    if not form.validate():
        return render_template("kuntosaliharjoitukset/new.html", form = form)
    sali = Salikerta(form.pvm.data, form.aika.data)
    sali.account_id = current_user.id

    db.session.add(sali)
    db.session().commit()
    form = Salikerta_LiikeForm()
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()

    return render_template("salikerta_liike/new.html", sali_id = sali.id, form = form)

# Salikerta_liike toiminnallisuudet:

# uuden rivin lisääminen liitostauluun salikerta - saliliike
@app.route("/salikerta_liike/<sali_id>/new/", methods=["POST"])
@login_required(role="USER")
def salikerta_liike_create(sali_id):
    form = Salikerta_LiikeForm(request.form)
    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(sali_id)
    if not form.validate():
        print("tässä formin data: ", form.liike.data)
        form = Salikerta_LiikeForm()
        form.liike.choices = Saliliike.hae_kaikki_liikkeet()
        return render_template("salikerta_liike/new.html", sk_liikkeet = liikkeet, 
            sali_id = sali_id, form = form)
    sl = Salikerta_liike(sali_id, form.liike.data, form.painot.data, form.toistot.data)
    db.session().add(sl)
    db.session().commit()
    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(sali_id)

    form = Salikerta_LiikeForm()
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()

    return render_template("salikerta_liike/new.html", sk_liikkeet = liikkeet, 
        sali_id = sali_id, form = form)

# rivin poistaminen liitostaulusta
@app.route("/salikerta_liike/<salikerta_liike_id>/delete", methods=["POST"])
@login_required()
def salikerta_liike_delete(salikerta_liike_id):
    sl = Salikerta_liike.query.get(salikerta_liike_id)

    salikerta_id = sl.salikerta_id
    db.session.delete(sl)
    db.session().commit()

    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(salikerta_id)

    form = Salikerta_LiikeForm()
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()

    return render_template("salikerta_liike/new.html", sk_liikkeet = liikkeet, 
        sali_id = salikerta_id, form = form)

# liitostaulun rivin päivitysform
@app.route("/salikerta_liike/<salikerta_liike_id>/edit", methods=["GET"])
@login_required()
def salikerta_liike_updateform(salikerta_liike_id):
    salikerta_liike = Salikerta_liike.query.get(salikerta_liike_id)
    form = Salikerta_LiikeForm(obj=salikerta_liike)
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()
    return render_template("salikerta_liike/edit.html", salikerta_liike=salikerta_liike, form = form)

# liitostaulun rivin päivitys
@app.route("/salikerta_liike/<salikerta_liike_id>/edit/", methods=["POST"])
@login_required()
def salikerta_liike_edit(salikerta_liike_id):
    form = Salikerta_LiikeForm(request.form)
    sl = Salikerta_liike.query.get(salikerta_liike_id)
    
    if not form.validate():
        return render_template("salikerta_liike/edit.html", salikerta_liike=sl, form = form)
    sl.liike = form.liike.data
    sl.saliliike_id = Saliliike.hae_liike_id(str(sl.liike))
    sl.saliliike_id = (sl.saliliike_id[0])['id']
    sl.toistot = form.toistot.data
    sl.painot = form.painot.data
    db.session().commit()
    liikkeet = Salikerta_liike.kaikki_salikerta_liikkeet(sl.salikerta_id)
    form = Salikerta_LiikeForm()
    form.liike.choices = Saliliike.hae_kaikki_liikkeet()
    return render_template("salikerta_liike/new.html", sk_liikkeet = liikkeet, 
        sali_id = sl.salikerta_id, form = form)


# Saliliikkeille toiminnallisuudet:

# saliliikkeen poisto tietokannasta
@app.route("/kuntosaliliikkeet/<liike_id>/delete", methods=["POST"])
@login_required()
def saliliike_delete(liike_id):
    s = Saliliike.query.get(liike_id)

    db.session.delete(s)
    db.session().commit()

    return redirect(url_for("saliliike_list"))

# saliliikkeen päivitysformin luonti
@app.route("/kuntosaliliikkeet/<liike_id>/", methods=["GET"])
@login_required()
def saliliike_updateform(liike_id):
    liike = Saliliike.query.get(liike_id)
    form = SaliliikeForm(obj=liike)
    return render_template("kuntosaliliikkeet/edit.html", liike=liike, form = form)

# saliliikkeen päivittäminen tietokannasta
@app.route("/kuntosaliliikkeet/<liike_id>/", methods=["POST"])
@login_required()
def saliliike_edit(liike_id):
    form = SaliliikeForm(request.form)
    liike = Saliliike.query.get(liike_id)

    if not form.validate():
        return render_template("kuntosaliliikkeet/edit.html", liike=liike, form = form)

    liike.nimi = form.nimi.data
    db.session().commit()

    liikkeet = Saliliike.query.all()
    return render_template("kuntosaliliikkeet/list.html", saliliikkeet=liikkeet, form = SaliliikeForm())

# kaikkien saliliikkeiden listaaminen
@app.route("/kuntosaliliikkeet/list/")
@login_required(role="USER")
def saliliike_list():
    return render_template("kuntosaliliikkeet/list.html", saliliikkeet = Saliliike.query.all(), form = SaliliikeForm())

# Uuden saliliikkeen luominen
@app.route("/kuntosaliliikkeet/new/", methods=["POST"])
@login_required(role="USER")
def saliliike_create():
    form = SaliliikeForm(request.form)

    if not form.validate():
        return render_template("kuntosaliliikkeet/list.html", saliliikkeet = Saliliike.query.all(), form = form)
    
    s = Saliliike(form.nimi.data)

    db.session().add(s)
    db.session().commit()

    liikkeet = Saliliike.query.all()

    return render_template("kuntosaliliikkeet/list.html", saliliikkeet=liikkeet, form = SaliliikeForm())