from application import db
import datetime
from decimal import *


class Base(db.Model):

    __abstract__ = True
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

class Harjoitus(Base):

    __abstract__ = True

    pvm = db.Column(db.Date, nullable=False)
    aika = db.Column(db.Time, nullable=False)

class juoksu_print():
    def __init__(self, id, pvm, aika, matka):
      self.id = id
      self.pvmstring = str(pvm).replace('-', '.')
      self.aikastring = aika
      self.matkastring = str(matka) + " km"     

class sali_print():
    def __init__(self, id, pvm, aika):
      self.id = id
      self.pvmstring = str(pvm).replace('-', '.')
      self.aikastring = aika

class salikerta_liike_print():
    def __init__(self, id, liike, painot, toistot):
        self.id = id
        self.liike = liike
        self.painot = str(painot) + " kg"
        self.toistot = toistot
        self.form = round(float(painot) * (toistot ** 0.1), 2))

class sali_print_admin(sali_print):
    def __init__(self, id, pvm, aika, user):
        sali_print.__init__(self, id, pvm, aika)
        self.user = user

class juoksu_print_admin(juoksu_print):
    def __init__(self, id, pvm, aika, matka, user):
        juoksu_print.__init__(self, id, pvm, aika, matka)
        self.user = user