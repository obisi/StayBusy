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


    # hakee kaikki harjoitukset kahden päivämäärän väliltä tietyltä käyttäjältä
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

    # hakee kaikki tietokannan harjoitukset tietyltä aikaväliltä
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