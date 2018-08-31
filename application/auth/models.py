from application import db
from application.models import Base
import datetime
from application.models import salikerta_liike_print

from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(144), nullable=False)

    juoksut = db.relationship("Juoksu", backref='account', lazy=True)
    harjoitukset = db.relationship("Salikerta", backref='account', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.role = "USER"
  
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
        stmt = text("SELECT MAX(Juoksu.matka) FROM Juoksu")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"matka":row[0]})
        return response

    @staticmethod
    def pisin_juoksu_oma(kayttaja_id):
        stmt = text("SELECT MAX(Juoksu.matka) FROM Juoksu" 
        " WHERE Juoksu.account_id = :kayttaja_id"
        " GROUP BY Juoksu.matka").params(kayttaja_id = kayttaja_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"matka":row[0]})
        return response
    @staticmethod
    def kenen_juoksu(juoksu_id):
        stmt = text("SELECT Account.name FROM Account"
                    " INNER JOIN Juoksu ON Juoksu.account_id = Account.id"
                    " WHERE Juoksu.id = :juoksu_id"
                    " GROUP BY Account.name").params(juoksu_id=juoksu_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(row[0])
        return response
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
        



    

    @staticmethod
    def kaikki_juoksut(kayttaja_id):
        stmt = text("SELECT Juoksu.id, Juoksu.pvm, Juoksu.matka, Juoksu.aika FROM Juoksu"
                     " WHERE Juoksu.account_id = :kayttaja_id"
                     " GROUP BY Juoksu.id").params(kayttaja_id=kayttaja_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "pvm":row[1], "matka":row[2], "aika":row[3]})
        return response
    
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


    @staticmethod
    def kaikki_harjoitukset_pvm(kayttaja_id, pvmEka, pvmToka):
        if pvmEka == None or pvmToka == None:
            return [],[]

        stmt = text("SELECT Juoksu.id, Juoksu.pvm, Juoksu.matka, Juoksu.aika FROM Juoksu"
                     " WHERE Juoksu.account_id = :kayttaja_id AND Juoksu.pvm >= :pvmEka"
                     " AND Juoksu.pvm <= :pvmToka"
                     " GROUP BY Juoksu.id").params(kayttaja_id=kayttaja_id, pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseJ = []
        for row in res:
            responseJ.append({"id":row[0], "pvm":row[1], "matka":row[2], "aika":row[3]})  
     
        stmt = text("SELECT Salikerta.id, Salikerta.pvm, Salikerta.aika FROM Salikerta"
                     " WHERE Salikerta.account_id = :kayttaja_id AND Salikerta.pvm >= :pvmEka"
                     " AND Salikerta.pvm <= :pvmToka"
                     " GROUP BY Salikerta.id ").params(kayttaja_id=kayttaja_id, pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseS = []
        for row in res:
            responseS.append({"id":row[0], "pvm":row[1], "aika":row[2]})
        return responseJ, responseS

    @staticmethod
    def kaikki_harjoitukset_pvm_admin(pvmEka, pvmToka):
        if pvmEka == None or pvmToka == None:
            return [],[]

        stmt = text("SELECT Juoksu.id, Juoksu.pvm, Juoksu.matka, Juoksu.aika FROM Juoksu"
                     " WHERE Juoksu.pvm >= :pvmEka AND Juoksu.pvm <= :pvmToka"
                     " GROUP BY Juoksu.id").params(pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseJ = []
        for row in res:
            responseJ.append({"id":row[0], "pvm":row[1], "matka":row[2], "aika":row[3]})  
     
        stmt = text("SELECT Salikerta.id, Salikerta.pvm, Salikerta.aika FROM Salikerta"
                     " WHERE Salikerta.pvm >= :pvmEka AND Salikerta.pvm <= :pvmToka"
                     " GROUP BY Salikerta.id ").params(pvmEka = pvmEka, pvmToka=pvmToka)
        res = db.engine.execute(stmt)

        responseS = []
        for row in res:
            responseS.append({"id":row[0], "pvm":row[1], "aika":row[2]})
        return responseJ, responseS

    @staticmethod
    def kaikki_salikerta_liikkeet(salikerta_id):
        stmt = text("SELECT Salikerta_liike.id, Saliliike.nimi, Salikerta_liike.painot, Salikerta_liike.toistot FROM Salikerta_liike"
                     " INNER JOIN Salikerta ON Salikerta_liike.salikerta_id = Salikerta.id "
                     " INNER JOIN Saliliike ON Salikerta_liike.saliliike_id = Saliliike.id "
                     " WHERE Salikerta.id = :salikerta_id "
                     " GROUP BY Salikerta_liike.id ").params(salikerta_id=salikerta_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(salikerta_liike_print(row[0], row[1], row[2], row[3]))
        return response
    