from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class UserForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, message="Vähintään 2 merkkiä pitkä")])
    username = StringField("Username", [validators.Length(min=2, message="Vähintään 2 merkkiä pitkä")])
    password = PasswordField("Password", [validators.Length(min=5, message="Vähintään 5 merkkiä pitkä")])
    
  
    class Meta:
        csrf = False