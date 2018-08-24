from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms import IntegerField, validators
from wtforms import DateField, validators
from wtforms import TimeField, validators

class SaliForm(FlaskForm):
    pvm = DateField("Päivämäärä (pp.kk.vvvv)", format='%d.%m.%Y')
    aika = TimeField("Kesto (tt:mm:ss)", format='%H:%M:%S')
 
    class Meta:
        csrf = False