from flask_wtf import FlaskForm
from application import app, db
#from application.kuntosaliharjoitukset.models import Harjoitus_Liike
from wtforms import StringField, validators
from wtforms import IntegerField, validators
from wtforms import DateField, validators
from wtforms import TimeField, validators
from wtforms import SelectField, validators

class SaliForm(FlaskForm):
    pvm = DateField("Päivämäärä (pp.kk.vvvv)", format='%d.%m.%Y')
    aika = TimeField("Kesto (tt:mm:ss)", format='%H:%M:%S')

    class Meta:
        csrf = False

# class Salikerta_LiikeForm(FlaskForm):
#     saliliikkeet = Saliliike.query.all()
#     liikkeet = []
#     for liike in saliliikkeet:
#         liikkeet.append(liike.nimi)
#     liike = SelectField('Liike', choices = liikkeet)
#     paino = IntegerField('Paino: ')
#     toistot = IntegerField('Toistot: ')

#     class Meta:
#         csrf = False