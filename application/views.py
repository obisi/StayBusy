import datetime
from flask import Flask, render_template
app = Flask(__name__)
from application import app
from application.auth.models import User
from flask_login import current_user
from application import app, db, login_manager, login_required


@app.route("/")
def hello():
    if current_user.is_authenticated:
        juoksu = User.pisin_juoksu()
        if not juoksu:
            return render_template("index.html")
        juoksu=juoksu[0]
        oma_juoksu = User.pisin_juoksu_oma(current_user.id)
        print(oma_juoksu)
        if not oma_juoksu:
            return render_template("index.html", juoksu = str(juoksu['matka']) + " km", omajuoksu = "Lenkille siitä!" )
        oma_juoksu = oma_juoksu[0]
        return render_template("index.html", juoksu = str(juoksu['matka']) + " km", omajuoksu = str(oma_juoksu['matka']) + " km" )

    else:
        return render_template("index.html")


