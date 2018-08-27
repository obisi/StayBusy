from application import db
from application.models import Harjoitus
from application.models import Base
import datetime

# class Harjoitus_Liike(Base):
#     __tablename__ = 'harjoitus_liike'

#     Salikerta_id = db.Column(db.Integer, db.ForeignKey('Salikerta.id'), primary_key=True)
#     Saliliike_id = db.Column(db.Integer, db.ForeignKey('Saliliike.id'), primary_key=True)
#     painot = db.Column(db.Integer)
#     toistot = db.Column(db.Integer)

#     Salikerta = db.relationship("Salikerta", back_populates='Saliliike', lazy=True)
#     Saliliike = db.relationship("Saliliike", back_populates='Salikerta', lazy=True)

#     def __init__(self, salikerta, saliliike, painot, toistot):
#         self.Salikerta_id = salikerta.id
#         self.Saliliike_id = saliliike.id
#         self.painot = painot
#         self.toistot = toistot

class Salikerta(Harjoitus):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    # harjoitus_liike = db.relationship('Harjoitus_Liike', back_populates='Salikerta', cascade='delete', lazy=True)


    def __init__(self,pvm, aika):
        
        self.pvm=pvm
        self.aika = aika

