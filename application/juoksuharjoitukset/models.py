from application import db
from application.models import Harjoitus
from application.models import Base
import datetime
from sqlalchemy.sql import text

class Juoksu(Harjoitus):
    matka = db.Column(db.DECIMAL(6,2), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)


    def __init__(self, pvm, matka, aika):
        
        self.pvm=pvm
        self.matka = matka
        self.aika = aika

    # hakee pisimmän juoksun tietokannasta
    @staticmethod
    def pisin_juoksu():
        stmt = text("SELECT MAX(Juoksu.matka) FROM Juoksu")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"matka":row[0]})
        return response

    # hakee käyttäjän pisimmän juoksun tietokannasta
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

    # palauttaa juoksun käyttäjän nimen
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

    # palauttaa käyttäjän kaikki juoksut
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

