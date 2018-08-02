import datetime
from flask import Flask, render_template
app = Flask(__name__)
from application import app

class juoksu:
    def __init__(self, pvm, metrit, sekunnit, juoksija):
        self.pvm = pvm
        self.matka = str(round(metrit / 1000, 2)) + " km"
        self.aika = str(datetime.timedelta(seconds=sekunnit))
        self.juoksija = juoksija

tietoja = "Juoksusi: "

linkit = ["Yksi linkki", "Toinen linkki", "Kolmas linkki"]

juoksut = []

juoksut.append(juoksu("10.7.2018", 6000, 3600, "Matti"))
juoksut.append(juoksu("13.7.2018", 7000, 3600, "Matti"))
juoksut.append(juoksu("16.7.2018", 8000, 3600, "Matti"))

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/juoksudata")
def content():
    return render_template("juoksudata.html",tietoja=tietoja, linkit=linkit, juoksut=juoksut)
