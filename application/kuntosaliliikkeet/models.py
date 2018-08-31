from application import db
from application.models import Base
from application.kuntosaliharjoitukset import models

from sqlalchemy.sql import text

class Saliliike(Base):
    
    nimi = db.Column(db.String(144), nullable=False)
    salikerta_liike = db.relationship('Salikerta_liike', 
                        cascade='delete', lazy=True)


    def __init__(self, nimi):
        self.nimi = nimi
    def __repr__(self):
        return self.nimi

    @staticmethod
    def hae_liike_id(saliliike_nimi):
        stmt = text("SELECT Saliliike.id FROM Saliliike"
                     " WHERE Saliliike.nimi = :saliliike_nimi"
                     " GROUP BY Saliliike.id").params(saliliike_nimi=saliliike_nimi)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0]})
        return response


    @staticmethod
    def hae_liike_nimi(saliliike_id):
        stmt = text("SELECT Saliliike.nimi FROM Saliliike"
                     " WHERE Saliliike.id = :saliliike_id"
                     " GROUP BY Saliliike.id").params(saliliike_id=saliliike_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"nimi":row[0]})
        return response

    @staticmethod
    def hae_kaikki_liikkeet():
        stmt = text("SELECT Saliliike.id, Saliliike.nimi FROM Saliliike")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append((row[0], row[1]))
        return response

