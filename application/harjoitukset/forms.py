from flask_wtf import FlaskForm
from wtforms import DateField, validators

class Pvmhaku_Form(FlaskForm):
    pvmEka = DateField("Mistä (pp.kk.vvvv)", format='%d.%m.%Y')
    pvmToka = DateField("Mihin (pp.kk.vvvv)", format='%d.%m.%Y')

    class Meta:
        csrf = False