from app import db, login_manager
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    flight = db.relationship('Flights_Creation', backref='user', lazy=True, cascade="all, delete-orphan")

class Flights_Creation(db.Model):
    __tablename__ = "User_Flights"
    f_id = db.Column(db.Integer, primary_key = True)
    airline_type = db.Column(db.String(50),nullable = False)
    depurture_time = db.Column(db.String(50), default=str(datetime.datetime.now().strftime("%H:%M:%S")))
    arrival_time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), default=str(datetime.datetime.now().date()))
    From = db.Column(db.String(30),nullable=False)
    To = db.Column(db.String(30),nullable=False)
    ticket_price = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(30),nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("Users.id"),nullable=False)
