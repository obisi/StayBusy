from application import db
from application.models import Harjoitus
from application.models import Base
import datetime

""" liikkeet_table = db.Table('harjoitus_liike',
    db.Column("id", db.Integer, primary_key=True),
    db.Column("salikerta_id", db.Integer, 
        db.ForeignKey("salikerta.id")),
    db.Column("saliliike_id", db.Integer, 
        db.ForeignKey("saliliike.id")),
    db.Column("toistot", db.Integer, nullable=False),
    db.Column("painot", db.Integer, nullable=False)
) """

class Salikerta(Harjoitus):
    pvmstring = db.Column(db.String(10), nullable=False)
    aikastring = db.Column(db.String(20), nullable=False)

    
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#     liikkeet = db.relationship('Saliliike', secondary=liikkeet_table, backref=db.backref('harjoitukset', lazy='dynamic'))


    def __init__(self, pvm, tunnit, minuutit, sekunnit):
        sec = int(tunnit) * 3600 + int(minuutit) * 60 + sekunnit
        self.pvm=pvm
        self.pvmstring = str(pvm).replace('-', '.')
        self.aika = sec
        self.aikastring = str(datetime.timedelta(seconds=sec))
