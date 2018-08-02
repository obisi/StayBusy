from application import db
import datetime

class Juoksu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pvm = db.Column(db.String(144), nullable=False)
    matka = db.Column(db.Integer, nullable=False)
    aika = db.Column(db.Integer, nullable=False)



    def __init__(self, pvm, matka, aika):
        self.pvm = pvm
        self.matka = matka
        self.aika = aika
