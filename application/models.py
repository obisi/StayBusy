from application import db
import datetime

class Base(db.Model):

    __abstract__ = True
  
    id = db.Column(db.Integer, primary_key=True)
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