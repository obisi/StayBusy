from application import app, db
from flask import redirect, render_template, request, url_for
from application.harjoitukset.models import Juoksu
from application.harjoitukset.forms import JuoksuForm
from flask_login import login_required, current_user
import datetime

@app.route("/harjoitukset/<juoksu_id>/delete", methods=["POST"])
@login_required
def juoksu_delete(juoksu_id):
    j = Juoksu.query.get(juoksu_id)

    db.session.delete(j)
    db.session().commit()

    return redirect(url_for("juoksut_index"))

@app.route("/harjoitukset/", methods=["GET"])
@login_required
def juoksut_index():
    return render_template("harjoitukset/list.html", juoksut = Juoksu.query.all())

@app.route("/harjoitukset/<juoksu_id>/single", methods=["GET"])
@login_required
def juoksu_single(juoksu_id):
    return render_template("harjoitukset/single.html", juoksu = Juoksu.query.get(juoksu_id))


@app.route("/harjoitukset/<juoksu_id>/", methods=["GET"])
@login_required
def juoksu_updateform(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    return render_template("harjoitukset/edit.html", j=j, form = JuoksuForm())

@app.route("/harjoitukset/<juoksu_id>/", methods=["POST"])
@login_required
def juoksu_edit(juoksu_id):
    form = JuoksuForm(request.form)
    j = Juoksu.query.get(juoksu_id)

    if not form.validate():
        return render_template("harjoitukset/edit.html", j=j, form = form)

    j.pvm = form.pvm.data
    j.matka = form.matka.data
    j.aika = form.tunnit.data * 3600 + form.minuutit.data * 60 + form.sekunnit.data
    j.aikaString = str(datetime.timedelta(seconds=j.aika))
    j.matkaString = str(round(j.matka / 1000, 2)) + " km"

    db.session().commit()
    return redirect(url_for("juoksut_index"))


@app.route("/harjoitukset/new/")
@login_required
def juoksut_form():
    return render_template("harjoitukset/new.html", form = JuoksuForm())

@app.route("/harjoitukset/", methods=["POST"])
@login_required
def juoksut_create():
    form = JuoksuForm(request.form)

    if not form.validate():
        return render_template("harjoitukset/new.html", form = form)

    j = Juoksu(form.pvm.data, form.matka.data, form.tunnit.data, form.minuutit.data, form.sekunnit.data)
    j.account_id = current_user.id

    db.session().add(j)
    db.session().commit()

    return redirect(url_for("juoksut_create"))