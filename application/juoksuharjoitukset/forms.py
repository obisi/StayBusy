from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms import IntegerField, validators
from wtforms import DateField, validators
from wtforms import TimeField, validators
from wtforms import DecimalField, validators

class JuoksuForm(FlaskForm):
    pvm = DateField("Päivämäärä (pp.kk.vvvv)", format='%d.%m.%Y')
    aika = TimeField("Kesto (tt:mm:ss)", format='%H:%M:%S')
    matka = DecimalField("Matka (km)", [validators.NumberRange(min=0, max=10000, message="Virheellinen syöte")], places=2)
    # info = StringFrield("Lisätietoja juoksusta: ")
    # matka = IntegerField("Matka (metriä)", [validators.NumberRange(min=0, max=100000000, message = "Lisää juostu matka")])
    # tunnit = IntegerField("Tunnit", [validators.NumberRange(min=0, max=100000, message="Ei negatiivisia arvoja")])
    # minuutit = IntegerField("Minuutit", [validators.NumberRange(min=0,max=59,message="Anna väliltä 00-59")])
    # sekunnit = IntegerField("Sekunnit", [validators.NumberRange(min=0,max=59,message="Anna väliltä 00-59")])
 
    class Meta:
        csrf = False