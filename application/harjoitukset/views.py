from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.juoksuharjoitukset.models import Juoksu
from application.juoksuharjoitukset.forms import JuoksuForm
from application.kuntosaliharjoitukset.models import Salikerta
from application.kuntosaliharjoitukset.forms import SaliForm
from application.harjoitukset.forms import Pvmhaku_Form
from flask_login import login_required, current_user
import datetime


@app.route("/harjoitukset/", methods=["GET"])
@login_required
def harjoitukset_index():
    return render_template("/harjoitukset/list.html", juoksut = User.kaikki_juoksut(current_user.id), salit = User.kaikki_salikerrat(current_user.id))

@app.route("/harjoitukset/etsi_pvm/", methods=["GET"])
@login_required
def pvmhaku_form():
    return render_template("harjoitukset/etsi_pvm.html", form=Pvmhaku_Form)

@app.route("/harjoitukset/etsi_pvm/", methods=["POST"])
@login_required
def pvmhaku():
    form = Pvmhaku_Form(request.form)
    pvmEka = form.pvmEka.data
    pvmToka = form.pvmToka.data
    j, s = User.kaikki_harjoitukset_pvm(current_user.id, pvmEka, pvmToka)

    return render_template("harjoitukset/etsi_pvm.html", form=form, juoksut=j, salit=s)


## Juoksuille toiminnallisuudet

@app.route("/juoksuharjoitukset/<juoksu_id>/delete", methods=["POST"])
@login_required
def juoksu_delete(juoksu_id):
    j = Juoksu.query.get(juoksu_id)

    db.session.delete(j)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

@app.route("/juoksuharjoitukset/<juoksu_id>/single", methods=["GET"])
@login_required
def juoksu_single(juoksu_id):
    return render_template("juoksuharjoitukset/single.html", juoksu = Juoksu.query.get(juoksu_id))


@app.route("/juoksuharjoitukset/<juoksu_id>/", methods=["GET"])
@login_required
def juoksu_updateform(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    form = JuoksuForm(obj=j)
    m, s = divmod(j.aika, 60)
    h, m = divmod(m, 60)
    form.tunnit.data = h
    form.minuutit.data = m
    form.sekunnit.data = s
    return render_template("juoksuharjoitukset/edit.html", j=j, form = form)

@app.route("/juoksuharjoitukset/<juoksu_id>/", methods=["POST"])
@login_required
def juoksu_edit(juoksu_id):
    form = JuoksuForm(request.form)
    j = Juoksu.query.get(juoksu_id)

    if not form.validate():
        return render_template("juoksuharjoitukset/edit.html", j=j, form = form)

    j.pvmString =  str(form.pvm.data).replace('-', '.')
    j.pvm = form.pvm.data
    j.matka = form.matka.data
    j.aika = form.tunnit.data * 3600 + form.minuutit.data * 60 + form.sekunnit.data
    j.aikaString = str(datetime.timedelta(seconds=j.aika))
    j.matkaString = str(round(j.matka / 1000, 2)) + " km"

    db.session().commit()
    return redirect(url_for("harjoitukset_index"))


@app.route("/juoksuharjoitukset/new/")
@login_required
def juoksut_form():
    return render_template("juoksuharjoitukset/new.html", form = JuoksuForm())

@app.route("/juoksuharjoitukset/", methods=["POST"])
@login_required
def juoksut_create():
    form = JuoksuForm(request.form)

    if not form.validate():
        return render_template("juoksuharjoitukset/new.html", form = form)

    j = Juoksu(form.pvm.data, form.matka.data, form.tunnit.data, form.minuutit.data, form.sekunnit.data)
    j.account_id = current_user.id

    db.session().add(j)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

## Saliharjoituksille toiminnallisuudet

@app.route("/kuntosaliharjoitukset/<sali_id>/delete", methods=["POST"])
@login_required
def sali_delete(sali_id):
    s = Salikerta.query.get(sali_id)

    db.session.delete(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))

@app.route("/kuntosaliharjoitukset/<sali_id>/single", methods=["GET"])
@login_required
def sali_single(sali_id):
    return render_template("kuntosaliharjoitukset/single.html", sali = Salikerta.query.get(sali_id))


@app.route("/kuntosaliharjoitukset/<sali_id>/", methods=["GET"])
@login_required
def sali_updateform(sali_id):
    sali = Salikerta.query.get(sali_id)
    form = SaliForm(obj=sali)
    m, s = divmod(sali.aika, 60)
    h, m = divmod(m, 60)
    form.tunnit.data = h
    form.minuutit.data = m
    form.sekunnit.data = s
    return render_template("kuntosaliharjoitukset/edit.html", sali=sali, form = form)

@app.route("/kuntosaliharjoitukset/<sali_id>/", methods=["POST"])
@login_required
def sali_edit(sali_id):
    form = JuoksuForm(request.form)
    sali = Salikerta.query.get(sali_id)

    if not form.validate():
        return render_template("kuntosaliharjoitukset/edit.html", sali=sali, form = form)

    sali.pvmString =  str(form.pvm.data).replace('-', '.')
    sali.pvm = form.pvm.data
    sali.aika = form.tunnit.data * 3600 + form.minuutit.data * 60 + form.sekunnit.data
    sali.aikaString = str(datetime.timedelta(seconds=sali.aika))

    db.session().commit()
    return redirect(url_for("harjoitukset_index"))


@app.route("/kuntosaliharjoitukset/new/")
@login_required
def sali_form():
    return render_template("kuntosaliharjoitukset/new.html", form = SaliForm())

@app.route("/kuntosaliharjoitukset/", methods=["POST"])
@login_required
def sali_create():
    form = SaliForm(request.form)

    if not form.validate():
        return render_template("kuntosaliharjoitukset/new.html", form = form)

    s = Salikerta(form.pvm.data, form.tunnit.data, form.minuutit.data, form.sekunnit.data)
    s.account_id = current_user.id

    db.session().add(s)
    db.session().commit()

    return redirect(url_for("harjoitukset_index"))