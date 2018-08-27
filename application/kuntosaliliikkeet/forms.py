from flask_wtf import FlaskForm
from wtforms import StringField, validators

class SaliliikeForm(FlaskForm):
    nimi = StringField("Nimi: ", [validators.Length(min=2, message="Vähintään 2 merkkiä pitkä")])

    class Meta:
        csrf = False