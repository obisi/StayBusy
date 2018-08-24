from application import db
from application.models import Harjoitus
from application.models import Base
import datetime

class Juoksu(Harjoitus):
    #pvmstring = db.Column(db.String(10), nullable=False)
    matka = db.Column(db.DECIMAL(6,2), nullable=False)
    #aikastring = db.Column(db.String(20), nullable=False)
    #matkastring = db.Column(db.String(1500), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)


    def __init__(self, pvm, matka, aika):
        # sec = int(tunnit) * 3600 + int(minuutit) * 60 + sekunnit
        self.pvm=pvm
        # self.pvmstring = str(pvm).replace('-', '.')
        self.matka = matka
        self.aika = aika
        # self.aikastring = str(datetime.timedelta(seconds=sec))
        # self.matkastring = str(round(matka / 1000, 2)) + " km"

