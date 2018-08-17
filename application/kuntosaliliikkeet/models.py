from application import db
from application.models import Base

class Saliliike(Base):
    
    nimi = db.Column(db.String(144), nullable=False)

    def __init__(self, nimi):
        self.nimi = nimi

