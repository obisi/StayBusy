from application import db
from application.models import Harjoitus
from application.models import Base
import datetime

class Juoksu(Harjoitus):
    matka = db.Column(db.DECIMAL(6,2), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)


    def __init__(self, pvm, matka, aika):
        
        self.pvm=pvm
        self.matka = matka
        self.aika = aika

