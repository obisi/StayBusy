from application import db
from application.models import Harjoitus
from application.models import Base
import datetime

class Salikerta(Harjoitus):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    salikerta_liike = db.relationship(
        'Salikerta_liike', cascade='delete', lazy=True)


    def __init__(self,pvm, aika):
        
        self.pvm=pvm
        self.aika = aika



class Salikerta_liike(Base):
    salikerta_id = db.Column(db.Integer, db.ForeignKey('salikerta.id'),
                            primary_key=False)
    saliliike_id = db.Column(db.Integer, db.ForeignKey('saliliike.id'),
                            primary_key=False)
    painot = db.Column(db.DECIMAL(6,2), nullable=False)
    toistot = db.Column(db.Integer, nullable=False)

    salikerta = db.relationship("Salikerta", lazy=True)
    saliliike = db.relationship("Saliliike", lazy=True)

    def __init__(self, salikerta_id, saliliike_id, painot, toistot):
        self.salikerta_id = salikerta_id    
        self.saliliike_id = saliliike_id
        self.painot = painot
        self.toistot = toistot
        

    
   
