from application import db
from application.models import Base

class Saliliike(Base):
    
    nimi = db.Column(db.String(144), nullable=False)
    # harjoitus_liike = db.relationship("Harjoitus_Liike", back_populates='Saliliike', cascade='delete', lazy=True)


    def __init__(self, nimi):
        self.nimi = nimi

