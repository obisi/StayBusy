from flask_wtf import FlaskForm
from wtforms import StringField, validators

class SaliliikeForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, message="Vähintään 2 merkkiä pitkä")])