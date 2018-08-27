from application import app, db, login_manager, login_required
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.juoksuharjoitukset.models import Juoksu
from application.juoksuharjoitukset.forms import JuoksuForm
from application.kuntosaliharjoitukset.models import Salikerta
# from application.kuntosaliharjoitukset.models import Harjoitus_Liike
from application.kuntosaliharjoitukset.forms import SaliForm
#from application.kuntosaliharjoitukset.forms import Salikerta_LiikeForm
from application.kuntosaliliikkeet.models import Saliliike
from application.kuntosaliliikkeet.forms import SaliliikeForm
from application.harjoitukset.forms import Pvmhaku_Form
from flask_login import current_user
from application.models import juoksu_print, sali_print
from datetime import datetime




@app.route("/harjoitukset/", methods=["GET"])
@login_required()
def harjoitukset_index():
    if current_user.role=="ADMIN":
        juoksut = Juoksu.query.all()
        salit = Salikerta.query.all()
        jt = []
        for j in juoksut:
            jt.append(juoksu_print(j.id, j.pvm, j.aika, j.aika))
        st = []
        for s in salit:
            st.append(sali_print(s.id, s.pvm, s.aika))
    else:
        juoksut = User.kaikki_juoksut(current_user.id)
        salit = User.kaikki_salikerrat(current_user.id)
        jt = []
        for j in juoksut:
            jt.append(juoksu_print(j['id'], j['pvm'], j['aika'], j['matka']))
        st = []
        for s in salit:
            st.append(sali_print(s['id'], s['pvm'], s['aika']))

    
    return render_template("/harjoitukset/list.html", juoksut = jt, salit = st)


@app.route("/harjoitukset/etsi_pvm/", methods=["GET"])
@login_required()
def pvmhaku_form():
    return render_template("harjoitukset/etsi_pvm.html", form=Pvmhaku_Form())

@app.route("/harjoitukset/etsi_pvm/", methods=["POST"])
@login_required()
def pvmhaku():
    form = Pvmhaku_Form(request.form)
    pvmEka = form.pvmEka.data
    pvmToka = form.pvmToka.data
    juoksut, salit = User.kaikki_harjoitukset_pvm(current_user.id, pvmEka, pvmToka)
    jt = []
    for j in juoksut:
        jt.append(juoksu_print(j['id'], j['pvm'], str(j['aika'])[:-7], j['matka']))
    st = []
    for s in salit:
        st.append(sali_print(s['id'], s['pvm'], str(s['aika'])[:-7]))

    return render_template("harjoitukset/etsi_pvm.html", form=form, juoksut=jt, salit=st)


## Juoksuille toiminnallisuudet

@app.route("/juoksuharjoitukset/<juoksu_id>/delete", methods=["POST"])
@login_required()
def juoksu_delete(juoksu_id):
    j = Juoksu.query.get(juoksu_id)

    db.session.delete(j)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

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


@app.route("/juoksuharjoitukset/<juoksu_id>/", methods=["GET"])
@login_required()
def juoksu_updateform(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    form = JuoksuForm(obj=j)
    return render_template("juoksuharjoitukset/edit.html", j=j, form = form)

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
    return redirect(url_for("harjoitukset_index"))


@app.route("/juoksuharjoitukset/new/")
@login_required(role="USER")
def juoksut_form():
    form = JuoksuForm(pvm = datetime.today().date())
    return render_template("juoksuharjoitukset/new.html", form = form)

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

## Saliharjoituksille toiminnallisuudet

@app.route("/kuntosaliharjoitukset/<sali_id>/delete", methods=["POST"])
@login_required()
def sali_delete(sali_id):
    s = Salikerta.query.get(sali_id)

    db.session.delete(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

@app.route("/kuntosaliharjoitukset/<sali_id>/single", methods=["GET"])
@login_required()
def sali_single(sali_id):
    s = Salikerta.query.get(sali_id)
    us = sali_print(s.id, s.pvm, s.aika)
    return render_template("kuntosaliharjoitukset/single.html", sali = us)


@app.route("/kuntosaliharjoitukset/<sali_id>/", methods=["GET"])
@login_required()
def sali_updateform(sali_id):
    sali = Salikerta.query.get(sali_id)
    form = SaliForm(obj=sali)
    return render_template("kuntosaliharjoitukset/edit.html", sali=sali, form = form)

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
    return redirect(url_for("harjoitukset_index"))


@app.route("/kuntosaliharjoitukset/new/")
@login_required(role="USER")
def sali_form():
    return render_template("kuntosaliharjoitukset/new.html", form = SaliForm())

@app.route("/kuntosaliharjoitukset/", methods=["POST"])
@login_required(role="USER")
def sali_create():
    form = SaliForm(request.form)

    if not form.validate():
        return render_template("kuntosaliharjoitukset/new.html", form = form)
    
    s = Salikerta(form.pvm.data, form.aika.data)
    s.account_id = current_user.id

    db.session().add(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

@app.route("/kuntosaliharjoitukset/liikkeet/")
@login_required(role="USER")
def haroitus_liike_form():
    return render_template("kuntosaliharjoitukset/new.html", form = Salikerta_LiikeForm())

@app.route("/kuntosaliharjoitukset/liikkeet/", methods=["POST"])
@login_required(role="USER")
def harjoitus_liike_create():
    form = Salikerta_LiikeForm(request.form)

    if not form.validate():
        return render_template("kuntosaliharjoitukset/new.html", form = form)
    
    s = Salikerta(form.pvm.data, form.aika.data)
    s.account_id = current_user.id

    db.session().add(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))


# Saliliikkeille toiminnallisuudet:

@app.route("/kuntosaliliikkeet/<liike_id>/delete", methods=["POST"])
@login_required()
def saliliike_delete(liike_id):
    s = Saliliike.query.get(liike_id)

    db.session.delete(s)
    db.session().commit()

    return redirect(url_for("saliliike_list"))


@app.route("/kuntosaliliikkeet/<liike_id>/", methods=["GET"])
@login_required()
def saliliike_updateform(liike_id):
    liike = Saliliike.query.get(liike_id)
    form = SaliliikeForm(obj=liike)
    return render_template("kuntosaliliikkeet/edit.html", liike=liike, form = form)

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



@app.route("/kuntosaliliikkeet/list/")
@login_required(role="USER")
def saliliike_list():
    return render_template("kuntosaliliikkeet/list.html", saliliikkeet = Saliliike.query.all(), form = SaliliikeForm())


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