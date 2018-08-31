from flask_wtf import FlaskForm
from application import app, db
from application.kuntosaliliikkeet.models import Saliliike
from wtforms import StringField, validators
from wtforms import IntegerField, validators
from wtforms import DateField, validators
from wtforms import TimeField, validators
from wtforms import SelectField, validators
from wtforms import DecimalField, validators

class SaliForm(FlaskForm):
    pvm = DateField("Päivämäärä (pp.kk.vvvv)", format='%d.%m.%Y')
    aika = TimeField("Kesto (tt:mm:ss)", format='%H:%M:%S')

    class Meta:
        csrf = False

# Ei toiminut muuten:
class MySelectField(SelectField):
    def pre_validate(self, form):
        for v, _ in self.choices:
            if isinstance(v, int):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))



class Salikerta_LiikeForm(FlaskForm):
    
    liike = MySelectField(choices=Saliliike.hae_kaikki_liikkeet(),label="Liike: ")
    painot = DecimalField("Paino(kg): ", [validators.NumberRange(min=0, max=10000, message="Virheellinen syöte")], places=2)
    toistot = IntegerField('Toistot: ', [validators.NumberRange(min=1, max=1000, message="Vähintään 1 toisto")])

    class Meta:
        csrf = False