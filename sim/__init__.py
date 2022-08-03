import collections
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask('__name__', template_folder='sim/templates', static_folder='sim/static')
app.config['SECRET_KEY'] = "MuhammadArman"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_Demog.db'
app.config['CKEDITOR_PKG_TYPE'] = 'full'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

ckeditor = CKEditor(app)

login_manager = LoginManager(app)

from sim.penduduk.routes import Suser
from sim.admin.routes import Sadmin

app.register_blueprint(Sadmin)
app.register_blueprint(Suser)