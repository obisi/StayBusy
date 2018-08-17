import datetime
from flask import Flask, render_template
app = Flask(__name__)
from application import app
from application.auth.models import User
from flask_login import login_required, current_user


@app.route("/")
def hello():
    juoksu = User.pisin_juoksu()
    juoksu=juoksu[0]
    juoksuOma = User.pisin_juoksu_oma(current_user.id)
    juoksuOma = juoksuOma[0]
    return render_template("index.html", juoksu = juoksu["matkaString"], omajuoksu=juoksuOma["matkaString"])


