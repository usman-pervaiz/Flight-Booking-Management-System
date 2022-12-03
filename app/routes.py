from flask import request, jsonify, render_template, redirect, url_for
from app.models import User, Flights_Creation
#from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.form import LoginForm, RegistrationForm,FlightBookingForm, DeleteFlightForm, UpdateFlightForm, StatusSearchForm
from flask_login import login_required, current_user,login_user,logout_user
from app import app,db, bcrypt
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import datetime

@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    form = StatusSearchForm()
    flights = Flights_Creation.query.all()
    arrived_flight = Flights_Creation.query.filter_by(status="arrived")
    active_flight = Flights_Creation.query.filter_by(status="active")
    delay_flight = Flights_Creation.query.filter_by(status="delay")
    flights_length = {
        "Total length":len(list(flights)),
        "Arrived length": len(list(arrived_flight)),
        "Active length": len(list(active_flight)),
        "Delay length":len(list(delay_flight))
    }
    if form.validate_on_submit():
        user_status = str(form.status.data).lower()
        return render_template('deshboard.html',user=current_user,flights_length=flights_length,flights=flights,flag=True,user_status=user_status,form=form)
    return render_template('deshboard.html',user=current_user,flights_length=flights_length,flights=flights,form=form)
    # return jsonify (
    #     message = f"Welcome {user.name} to deshborad",
    #     status = 200
    # )


@app.route("/BookFlight",methods=["GET","POST"])
@login_required
def BookFlight():
    try:
        form = FlightBookingForm()
        if form.validate_on_submit():
            #print("Ha ye to ho raha h")
            airline_type = form.airline_type.data
            To = form.To.data
            From = form.From.data
            ticket_price = form.ticket_price.data
            status = str(form.status.data).lower()
            geolocator = Nominatim(user_agent="geoapiExercises")
  
           
            
            location = geolocator.geocode(To)
            

            tf = TimezoneFinder()

            # From the lat/long, get the tz-database-style time zone name (e.g. 'America/Vancouver') or None
            timezone_str = tf.certain_timezone_at(lat=location.latitude, lng=location.longitude)

            if timezone_str is None:
                return render_template('flightBooking.html',form=form,message="Arrival Location Not define")
            else:
                # Display the current time in that time zone
                timezone = pytz.timezone(timezone_str)
                dt = datetime.datetime.utcnow()
                
            flight = Flights_Creation(airline_type=airline_type,arrival_time=str(dt + timezone.utcoffset(dt))[11:19], From =From,To=To, 
                                        ticket_price=ticket_price,status=status,u_id =current_user.id)
            db.session.add(flight)
            db.session.commit()
            
            return redirect('BookFlight')
        # else:
        #     return jsonify(
        #         message="Method Not Allowed",
        #         status = 404
        #     )
    except Exception as err:
        return err
    return render_template('flightBooking.html',form=form)
    # return jsonify(
    #     message="Fligh Booked",
    #     status=200
    # )

@app.route("/ShowFlights")
@login_required
def ShowFlights():
    try:
        flight_info = []
        # user_email = get_jwt_identity()
        # user = User.query.filter_by(id=user_email).first()
        flights = Flights_Creation.query.filter_by().all()
        
        for flight in flights:
            if flight.u_id == current_user.id:
                data = {
                    #"Owner" :current_user.name,
                    "Owner ID": current_user.id,
                    "Flight ID" : flight.f_id,
                    "Airplane Type" : flight.airline_type,
                    "Airplane Depurture" : flight.depurture_time,
                    "Airplane Arrival" : flight.arrival_time,
                    "To":flight.To,
                    "From":flight.From,
                    "Ticket Price" : flight.ticket_price,
                    "Status" : flight.status
                }
                flight_info.append(data)
        # else:
        #     return jsonify(
        #         message = "Mthod Not Allowed",
        #         status=400
        #     )
        print(flight_info)
    except Exception as err:
        return err
    return render_template('ShowOneFlights.html',flight_info=flight_info)

    # return jsonify(
    #     message="All Users Find",
    #     status=200,
    #     data = flight_info
    # )


@app.route("/delete_flight",methods=["GET","POST"])
@login_required
def delete_flight():
    try:
        form = DeleteFlightForm()
        if form.validate_on_submit():
            user_id = form.user_id.data
            flight_id = form.flight_id.data
            # user_email = get_jwt_identity()
            # user = User.query.filter_by(email=user_email).first()
            #print(user.id)
            if int(user_id) != int(current_user.id):
                return render_template("delete_flight.html",message="User Not existed",form=form)
            else:
                Flights_Creation.query.filter_by(f_id=flight_id).delete()
                db.session.commit()
                return redirect(url_for("delete_flight"))
    except Exception as err:
        return err

    return render_template("delete_flight.html",message="User Deleted",form=form)
    # return jsonify(
    #     message="Users Flight Deleted Successfuly",
    #     status=200
    # )


@app.route("/upadte_flight",methods=["GET","POST"])
@login_required
def upadte_flight():
    try:
        form = UpdateFlightForm()
        if form.validate_on_submit():
            user_id = form.user_id.data
            flight_id = form.flight_id.data
            airline_type = form.airline_type.data
            To = form.To.data
            From = form.From.data
            ticket_price = form.ticket_price.data
            status = form.status.data

            #flight_id = request.form["flight_id"]
            # airline_type = request.form["airline_type"]
            # airline_depurture = request.form["airline_depurture"]
            # airline_arrival = request.form["airline_arrival"]
            # ticket_price = request.form["airline_arrival"]
            # user_email = get_jwt_identity()
            # user = User.query.filter_by(email=user_email).first()
            if int(user_id) != int(current_user.id):
                return render_template("UpdateUserFlight.html",form=form, message="User Not Found")
                # return jsonify(
                #     message="User Only update their fligh",
                #     status=400
                # )
            else:
                Flights_Creation.query.filter_by(f_id=flight_id).update(dict(airline_type=airline_type, From =From,To=To, 
                                                ticket_price=ticket_price,status=status,u_id =current_user.id))
                db.session.commit()
                return redirect(url_for("upadte_flight"))
    except Exception as err:
        return err
    return render_template("UpdateUserFlight.html",form=form)
    # return jsonify(
    #     message = "Users Flight Sucessfuly Updated",
    #     status = 200
    # )


@app.route("/ShowAllUsersFlights",methods=['GET',"POST"])
@login_required
def ShowAllUsersFlights():
    try:
        users = User.query.all()
        flights = Flights_Creation.query.all()
        lst = []
        for flight in flights:
            if flight.u_id !=current_user.id:
                new_dict = {
                    "Flight ID" : flight.f_id,
                    "AirPlane Type": flight.airline_type,
                        "AirPlane Depurture": flight.depurture_time,
                        "AirPlane Arrival": flight.arrival_time,
                        "Date":flight.date,
                        "To": flight.To,
                        "From" : flight.From,
                        "Ticket Price": flight.ticket_price,
                        "Status": flight.status
                        
                    }
                lst.append(new_dict)
        print(lst)

            #print(info_dict)
        # else:
        #     return jsonify(
        #         message="Method not Allowed",
        #         status=400
        #     )
        #print(info_dict)
    except Exception as err:
        return err
    return render_template('AllUserFlights.html',info_dict=lst)
    # return jsonify(
    #     message = "All Users Flights",
    #     status = 200,
    #     data=info_dict
    # )
'''
@app.route("/ShowStatusFlight")
@login_required
def  ShowFlightByStatus():
    return render_template('ShowFlightsbyStatus.html')


@app.route("/delete_users", methods = ["DELETE"])
@login_required
def delete_users():
    try:
        if request.method == "DELETE":
            email = request.form['email']
            user = User.query.filter_by(email=email).first()
            if user:
                User.query.filter(User.email == email).delete()
            else:
                return jsonify(
                    message="User ID not existed",
                    status = 400
                )
        else:
            return jsonify(
                    message="Method not Allowed",
                    status = 400
                )
       
    except Exception as err:
        return err
    return jsonify(
        message = "User deleted Successfuly",
        status = 200
        )



'''


@app.route("/",methods=["GET","POST"])
def login():
    try:
        form = LoginForm()
        # print(form)
        # print(form.validate_on_submit())
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                #access_token = create_access_token(identity=email)
                login_user(user)
                return redirect('/dashboard')
            else:
                return render_template('login.html',form=form, message="Login Failed")
                # return jsonify(
                #     message = "User not existed",
                #     status = 200
                # )
        # else:
        #     return jsonify(
        #         message = "Method not Allowed",
        #         status = 400
        #     )
    except Exception as err:
        return err
    
    return render_template('login.html',form=form)
    # return jsonify(
    #         message = "User Login",
    #         status=200,
    #         access_token = access_token
    # )
    

@app.route("/register",methods=["GET","POST"])
def regsiter():
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            check_user = User.query.filter_by(email=email).first()
            if check_user:
                return render_template('registration.html',form=form, message="User Already Existed")
                # return jsonify(
                #     message="User Already existed",
                #     status=404
                # )
           
            hash_password = bcrypt.generate_password_hash(password=password).decode("utf-8")
            user = User(name=name,email=email,password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
    except Exception as e:
        return e
    
    return render_template('registration.html',form=form)

    # return jsonify(
    #     message="User Created Successfuly",
    #     status=200
    # )
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
#     render_template(

# total_data = ""
# active_data = ""
# delya_active = ""
# arrive_data = ""
#     )