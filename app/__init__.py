from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = "This is Secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:usman@localhost:5432/FlightManagement"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

db = SQLAlchemy(app)
#jwt = JWTManager(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

csrf = CSRFProtect(app)
csrf.init_app(app)

from app import routes