from application import db
import datetime

class Juoksu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pvm = db.Column(db.String(10), nullable=False)
    matka = db.Column(db.Integer, nullable=False)
    aika = db.Column(db.Integer, nullable=False)
    aikaString = db.Column(db.String(20), nullable=False)
    matkaString = db.Column(db.String(20), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)


    def __init__(self, pvm, matka, tunnit, minuutit, sekunnit):
        sec = int(tunnit) * 3600 + int(minuutit) * 60 + sekunnit

        self.pvm = str(pvm).replace('-', '.')
        self.matka = matka
        self.aika = sec
        self.aikaString = str(datetime.timedelta(seconds=sec))
        self.matkaString = str(round(matka / 1000, 2)) + " km"

