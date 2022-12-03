from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField, SearchField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email: ",validators=[DataRequired(),Email()])
    password =  PasswordField("Password: ",validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    name = StringField("Name: ",validators=[DataRequired()])
    email = EmailField("Email: ",validators=[DataRequired(),Email()])
    password =  PasswordField("Password: ",validators=[DataRequired()])
    confirm_password =  PasswordField("Confirm Password: ",validators=[DataRequired(),EqualTo("password",message='Passwords must match')])
    submit = SubmitField("Sign Up")

class FlightBookingForm(FlaskForm):
    airline_type = StringField("Airline type: ",validators=[DataRequired()])
    From = StringField("From: ",validators=[DataRequired()])
    To = StringField("To: ",validators=[DataRequired()])
    ticket_price = IntegerField("Ticket price: ",validators=[DataRequired()])
    status = StringField("Status: ",validators=[DataRequired()])
    submit = SubmitField("Book Flight")

class DeleteFlightForm(FlaskForm):
    user_id = IntegerField("User ID: ",validators=[DataRequired()])
    flight_id = IntegerField("Flight ID: ",validators=[DataRequired()])
    submit = SubmitField("Cancel Flight")

class UpdateFlightForm(FlaskForm):
    user_id = IntegerField("User ID: ",validators=[DataRequired()])
    flight_id = IntegerField("Flight ID: ",validators=[DataRequired()])
    airline_type = StringField("Airline type: ",validators=[DataRequired()])
    From = StringField("From: ",validators=[DataRequired()])
    To = StringField("To: ",validators=[DataRequired()])
    ticket_price = IntegerField("Ticket price: ",validators=[DataRequired()])
    status = StringField("Status: ",validators=[DataRequired()])
    submit = SubmitField("Update Flight")


class StatusSearchForm(FlaskForm):
    status = SearchField("Status Search: ",validators=[DataRequired()])
    submit = SubmitField("Search")