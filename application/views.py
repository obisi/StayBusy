import datetime
from flask import Flask, render_template
app = Flask(__name__)
from application import app
from application.auth.models import User


@app.route("/")
def hello():
    juoksu = User.pisin_juoksu()
    juoksu=juoksu[0]
    return render_template("index.html", juoksu = juoksu["matkaString"])


