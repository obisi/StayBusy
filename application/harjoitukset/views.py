from application import app, db
from flask import redirect, render_template, request, url_for
from application.harjoitukset.models import Juoksu

@app.route("/harjoitukset/", methods=["GET"])
def juoksut_index():
    return render_template("harjoitukset/list.html", juoksut = Juoksu.query.all())

@app.route("/harjoitukset/<juoksu_id>/", methods=["GET"])
def juoksu_updateform(juoksu_id):
    j = Juoksu.query.get(juoksu_id)
    return render_template("harjoitukset/edit.html", j=j)

@app.route("/harjoitukset/<juoksu_id>/", methods=["POST"])
def juoksu_edit(juoksu_id):

    j = Juoksu.query.get(juoksu_id)
    j.pvm = request.form.get("pvm")
    j.matka = request.form.get("matka")
    j.aika = request.form.get("aika")

    db.session().commit()
    return redirect(url_for("juoksut_create"))


@app.route("/harjoitukset/new/")
def juoksut_form():
    return render_template("harjoitukset/new.html")

@app.route("/harjoitukset/", methods=["POST"])
def juoksut_create():
    juoksu = Juoksu(request.form.get("pvm"), request.form.get("matka"), request.form.get("aika"))

    db.session().add(juoksu)
    db.session().commit()

    return redirect(url_for("juoksut_create"))