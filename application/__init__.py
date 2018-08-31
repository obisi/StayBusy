from flask import Flask
app = Flask(__name__)
from flask_login import current_user

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///harjoitukset.db"    
    app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)



from os import urandom
#app.config["SECRET_KEY"] = urandom(32)
app.config["SECRET_KEY"] = 'supersecret'

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                user_role = current_user.role
                if user_role == role:
                    unauthorized = False

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from application import views

from application.juoksuharjoitukset import models
from application import models

from application.kuntosaliliikkeet import models
from application.kuntosaliharjoitukset import models

from application.auth import models
from application.auth import views

from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try: 
    db.create_all()
except:
    pass

from application.harjoitukset import views

