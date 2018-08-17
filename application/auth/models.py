from application import db
from application.models import Base
import datetime

from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)

    juoksut = db.relationship("Juoksu", backref='account', lazy=True)
    harjoitukset = db.relationship("Salikerta", backref='account', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def pisin_juoksu():
        stmt = text("SELECT MAX(Juoksu.matka), Juoksu.matkaString FROM Juoksu")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"matka":row[0], "matkaString":row[1]})
        return response

    @staticmethod
    def pisin_juoksu_oma(kayttaja_id):
        stmt = text("SELECT MAX(Juoksu.matka), Juoksu.matkaString FROM Juoksu" 
        " WHERE Juoksu.account_id = :kayttaja_id").params(kayttaja_id = kayttaja_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"matka":row[0], "matkaString":row[1]})
        return response

    

    @staticmethod
    def kaikki_juoksut(kayttaja_id):
        stmt = text("SELECT Juoksu.id, Juoksu.pvmString, Juoksu.matkaString, Juoksu.aikaString FROM Juoksu"
                     " WHERE Juoksu.account_id = :kayttaja_id").params(kayttaja_id=kayttaja_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "pvmString":row[1], "matkaString":row[2], "aikaString":row[3]})
        return response
    
    @staticmethod
    def kaikki_salikerrat(kayttaja_id):
        stmt = text("SELECT Salikerta.id, Salikerta.pvmString, Salikerta.aikaString FROM Salikerta"
                     " WHERE Salikerta.account_id = :kayttaja_id").params(kayttaja_id=kayttaja_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "pvmString":row[1], "aikaString":row[2]})
        return response


    @staticmethod
    def kaikki_harjoitukset_pvm(kayttaja_id, pvmEka, pvmToka):
        if pvmEka == None or pvmToka == None:
            return [],[]
        format_str = '%Y-%m-%d'

        stmt = text("SELECT Juoksu.id, Juoksu.pvmString, Juoksu.matkaString, Juoksu.aikaString, Juoksu.pvm FROM Juoksu"
                     " WHERE Juoksu.account_id = :kayttaja_id AND Juoksu.pvm >= :pvmEka"
                     " AND Juoksu.pvm <= :pvmToka").params(kayttaja_id=kayttaja_id, pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseJ = []
        for row in res:
            responseJ.append({"id":row[0], "pvmString":row[1], "matkaString":row[2], "aikaString":row[3], "pvm":row[4]})  

        
        stmt = text("SELECT Salikerta.id, Salikerta.pvmString, Salikerta.aikaString, Salikerta.pvm FROM Salikerta"
                     " WHERE Salikerta.account_id = :kayttaja_id AND Salikerta.pvm >= :pvmEka"
                     " AND Salikerta.pvm <= :pvmToka").params(kayttaja_id=kayttaja_id, pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseS = []
        for row in res:
            responseS.append({"id":row[0], "pvmString":row[1], "aikaString":row[2], "pvm":row[3]})
        return responseJ, responseS