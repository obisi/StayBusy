from application import db
from application.models import Harjoitus
from application.models import Base
from application.models import salikerta_liike_print
import datetime
from sqlalchemy.sql import text

class Salikerta(Harjoitus):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    salikerta_liike = db.relationship(
        'Salikerta_liike', cascade='delete', lazy=True)


    def __init__(self,pvm, aika):
        
        self.pvm=pvm
        self.aika = aika


    # palauttaa salikerran käyttäjän
    @staticmethod
    def kenen_sali(sali_id):
        stmt = text("SELECT Account.name FROM Account"
                    " INNER JOIN Salikerta ON Salikerta.account_id = Account.id"
                    " WHERE Salikerta.id = :sali_id"
                    " GROUP BY Account.name").params(sali_id=sali_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(row[0])
        return response

    # tulostaa kaikki käyttäjän salikerrat
    @staticmethod
    def kaikki_salikerrat(kayttaja_id):
        stmt = text("SELECT Salikerta.id, Salikerta.pvm, Salikerta.aika FROM Salikerta"
                     " WHERE Salikerta.account_id = :kayttaja_id"
                     " GROUP BY Salikerta.id ").params(kayttaja_id=kayttaja_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "pvm":row[1], "aika":row[2]})
        return response



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


    # palauttaa liitostaulusta ja saliliiketaulusta yhdistetyn rivin, jossa lukee saliliikkeen nimi, painot ja toistot
    @staticmethod
    def kaikki_salikerta_liikkeet(salikerta_id):
        stmt = text("SELECT Salikerta_liike.id, Saliliike.nimi, Salikerta_liike.painot, Salikerta_liike.toistot FROM Salikerta_liike"
                     " INNER JOIN Salikerta ON Salikerta_liike.salikerta_id = Salikerta.id "
                     " INNER JOIN Saliliike ON Salikerta_liike.saliliike_id = Saliliike.id "
                     " WHERE Salikerta.id = :salikerta_id "
                     " GROUP BY Salikerta_liike.id, Saliliike.nimi ").params(salikerta_id=salikerta_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(salikerta_liike_print(row[0], row[1], row[2], row[3]))
        return response
    
        

    
   
