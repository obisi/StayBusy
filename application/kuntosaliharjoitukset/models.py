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


    
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#     liikkeet = db.relationship('Saliliike', secondary=liikkeet_table, backref=db.backref('harjoitukset', lazy='dynamic'))


    def __init__(self,pvm, aika):
        
        self.pvm=pvm
        self.aika = aika

