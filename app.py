from flask import Flask, request, jsonify, g , render_template_string
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from flask_bcrypt import Bcrypt, check_password_hash  # Import Bcrypt for password hashing
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from celery import Celery
from flask_mail import Message  # Import Message from Flask-Mail
from flask_mail import Mail, Message
from flask import current_app
import redis
import json
from flask import Flask, render_template
from flask_caching import Cache
from celery.schedules import crontab
from flask_cors import CORS
import os
from flask import Response
import csv
import io



# vue_dist_folder = os.path.join(os.path.dirname(__file__), 'ticket-booking-app/public/index.html')
app = Flask(__name__, template_folder='ticket-booking-app/public')
bcrypt = Bcrypt()
password = 'secret' 

hashed = bcrypt.generate_password_hash(password) 

CORS(app)


app.config['SECRET_KEY'] = 'Hello123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Hello123456'  # Change this to a strong random value
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

# Set your Flask-Mail configuration
app.config['MAIL_SERVER'] = 'localhost'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 1025  # Replace with the appropriate port
app.config['MAIL_USE_TLS'] = False  # Use TLS for secure connection
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'  # Default sender address
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

mail = Mail(app)
# app.config['MAIL_MAX_EMAILS'] = None  # Limit the number of emails sent
# app.config['MAIL_ASCII_ATTACHMENTS'] = False  # Allow non-ASCII attachments
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize Redis for caching
#cache = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)
cache = Cache(app)
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})
#cache = cache(app)

db = SQLAlchemy(app)

jwt = JWTManager(app)

#CELERY_TIMEZONE = 'UTC'

celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'app.send_daily_reminder',  # Update with your task path
        'schedule': crontab(hour=14, minute=46),  # Schedule to run at 8:00 AM UTC
    },
    'send_monthly_report': {
        'task': 'app.send_monthly_report',  # Update with your task path
        'schedule': crontab(hour=14, minute=46),  # Schedule to run at 8:00 AM UTC
    }
}


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50))
#     user_bookings = db.relationship('Booking', back_populates='user')

# class Admin(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     username = db.Column(db.String(50))
#     password = db.Column(db.String(50))

# class Theatre(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     place = db.Column(db.String(50))
#     capacity = db.Column(db.Integer)
#     shows = db.relationship('Show', backref='theatre', lazy=True)

# class Show(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     tags = db.Column(db.String(50))
#     rating = db.Column(db.Integer)
#     theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
#     bookings = db.relationship('Booking', backref='show', lazy=True)
#     user_bookings = db.relationship('Booking', back_populates='show')
#     total_tickets = db.Column(db.Integer, default=0)
#     price = db.Column(db.Integer)
#     date = db.Column(db.String(50))

# class Booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     num_tickets = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
#     user = db.relationship('User', backref='bookings', foreign_keys=[user_id])
#     show = db.relationship('Show', backref='bookings', foreign_keys=[show_id])
#     amount = db.Column(db.Integer)
#     booking_date = db.Column(db.DateTime)    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    user_bookings = db.relationship('Booking', back_populates='user')

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    place = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    shows = db.relationship('Show', backref='theatre', lazy=True)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tags = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    show_bookings = db.relationship('Booking', backref='show', lazy=True)
    user_related_bookings = db.relationship('Booking', back_populates='show') 
    total_tickets = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer)
    date = db.Column(db.String(50))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_tickets = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    user = db.relationship('User', backref='bookings', foreign_keys=[user_id])
    related_show = db.relationship('Show', back_populates='show_bookings', foreign_keys=[show_id])
    amount = db.Column(db.Integer)
    booking_date = db.Column(db.DateTime)

# @app.route('/')
# def serve_vue_app():
#     return render_template('index.html') # correct this


@app.route("/", methods=['GET'])
def serve_vue_app():
    # Your logic to fetch data and prepare the JSON response for the home page goes here
    # data = {
    #     "user" : "OK"
    # }
    data = {
        "users": [
            {
                "type": "user",
                "description": "Login as User",
                "path": "/user/login"
            },
            {
                "type": "user",
                "description": "User Signup",
                "path": "/user/signup"
            },
            {
                "type": "admin",
                "description": "Login as Admin",
                "path": "/admin/login"
            },
            {
                "type": "admin",
                "description": "Admin Signup",
                "path": "/admin/signup"
            }
        ]
    }

    return jsonify(data)

# Signup route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # Default role is "user"

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # hashed_password = generate_password_hash(password, method="sha256")
    
    try:
        if role == "user":
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
        elif role == "admin":
            new_admin = Admin(username=username, password=password, email=email)
            db.session.add(new_admin)
        else:
            return jsonify({"message": "Invalid role"}), 400

        db.session.commit()
        return jsonify({"message": f"Successfully signed up as {role}"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {e}"}), 500

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity() 
    return jsonify({'message': f'User {user_id} has been logged out'})

# # Login route
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password") 
#     role = "admin" # data.get("role")  # Default role is "user"

#     if not username or not password:
#         return jsonify({"message": "Username and password are required"}), 400

#     user = None
#     if role == "user":
#         user = User.query.filter_by(username=username).first()
#     elif role == "admin":
#         # user = Admin.query.filter_by(username=username).first()
#         return jsonify({"message": "Invalid role"}), 400
#     else:
#         return jsonify({"message": "Invalid role"}), 400

#     if user and check_password_hash(user.password, password):
#         access_token = create_access_token(identity=user.id)
#         return jsonify({"access_token": access_token}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

# # Login route
# @app.route("/login", methods=["POST"])
# def login():
#   data = request.get_json()
#   username = data.get("username")
#   password = data.get("password")
#   role = "admin" #data.get("role", "user") # Get role from request

#   if not username or not password:
#     return jsonify({"message": "Username and password are required"}), 400

#   user = None
#   if role == "user":
#     user = User.query.filter_by(username=username).first() 
#   elif role == "admin":
#     user = Admin.query.filter_by(username=username).first()

#   if user and check_password_hash(user.password, password):
#     access_token = create_access_token(identity=user.id)
#     return jsonify({"access_token": access_token, "role" : role}), 200
#   else:
#     return jsonify({"message": "Invalid credentials"}), 401

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    # user = Admin.query.filter_by(username=username).first()
    if role == "user":
        user = User.query.filter_by(username=username).first()
    elif role == "admin":
        user = Admin.query.filter_by(username=username).first()
    else:
        return jsonify({"message": "Invalid role"}), 400

    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "role": role}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
# {
# 	"username": "username",
# 	"password": "password"
# }

# Theatre management routes
@app.route('/theatres', methods=['POST','GET'])
@jwt_required()
def create_theatre():
    # if request.method == 'POST':
    data = request.get_json()
    # Extract required data from the request and create a new theatre
    name = data.get('name')
    place = data.get('place')
    capacity = data.get('capacity')
    role = data.get('role')
        

    if not name or not place or not capacity:
        return jsonify({'message': 'Name, place, and capacity are required'}), 400

    if not role == 'admin':
        return jsonify({'message': 'Only admin can create theatres'}), 407

    try:
        theatre = Theatre(name=name, place=place, capacity=capacity)
        db.session.add(theatre)
        db.session.commit()
        return jsonify({'message': 'Theatre created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500
    
@app.route('/theatres-data', methods=['GET'])
def gettheatre():

# def get_theatre():
    theatres = Theatre.query.all()
    theatre_info = []
    for theatre in theatres:
        theatre_data = {
            "id" : theatre.id,
            "name" : theatre.name,
            "place" : theatre.place,
            "capacity" : theatre.capacity
        }
        theatre_info.append(theatre_data)
    return jsonify(theatre_info) , 200




@app.route('/theatres/<int:theatre_id>', methods=['GET', 'POST','PUT', 'DELETE'])
@jwt_required()
def edit_or_delete_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    if request.method == 'PUT':
        # if not g.user.is_admin:
        #     return jsonify({'message': 'Only admin can edit theatres'}), 403

        data = request.get_json()
        # Extract data for editing the theatre
        name = data.get('name')
        place = data.get('place')
        capacity = data.get('capacity')

        # Update theatre attributes
        if name:
            theatre.name = name
        if place:
            theatre.place = place
        if capacity:
            theatre.capacity = capacity

        try:
            db.session.commit()
            return jsonify({'message': 'Theatre updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

    elif request.method == 'DELETE':
        # if not g.user.is_admin:
        #     return jsonify({'message': 'Only admin can delete theatres'}), 403

        try:
            db.session.delete(theatre)
            db.session.commit()
            return jsonify({'message': 'Theatre deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

# Show management routes
@app.route('/shows', methods=['POST','GET'])
@jwt_required()
def create_show():
    data = request.get_json()
    # Extract required data from the request and create a new show
    name = data.get('name')
    tags = data.get('tags')
    rating = data.get('rating')
    theatre_id = data.get('theatre_id')
    total_tickets = data.get('total_tickets')
    price = data.get('price')
    date = data.get('date')

    if not name or not tags or not rating or not theatre_id or not total_tickets or not price or not date:
        return jsonify({'message': 'All fields are required'}), 400

    # if not g.user.is_admin:
    #     return jsonify({'message': 'Only admin can create shows'}), 403

    try:
        show = Show(name=name, tags=tags, rating=rating, theatre_id=theatre_id,
                    total_tickets=total_tickets, price=price, date=date)
        db.session.add(show)
        db.session.commit()
        return jsonify({'message': 'Show created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

@app.route('/show-data', methods=['GET'])
def getshow():

# def get_show():
    shows = Show.query.all()
    show_info = []
    for show in shows:
        show_data = {
            "id" : show.id,
            "name" : show.name,
            "tags" : show.tags,
            "rating" : show.rating,
            "theatre_id" : show.theatre_id,
            "total_tickets" : show.total_tickets,
            "price" : show.price,
            "date" : show.date
        }
        show_info.append(show_data)
    return jsonify(show_info) , 200


@app.route('/shows/<int:show_id>', methods=['GET','POST','PUT', 'DELETE'])
@jwt_required()
def edit_or_delete_show(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show not found'}), 404

    if request.method == 'PUT':
    #     if not role == 'admin':
    #         return jsonify({'message': 'Only admin can edit shows'}), 403

        data = request.get_json()
        # Extract data for editing the show
        name = data.get('name')
        tags = data.get('tags')
        rating = data.get('rating')
        theatre_id = data.get('theatre_id')
        total_tickets = data.get('total_tickets')
        price = data.get('price')
        date = data.get('date')

        # Update show attributes
        if name:
            show.name = name
        if tags:
            show.tags = tags
        if rating:
            show.rating = rating
        if theatre_id:
            show.theatre_id = theatre_id
        if total_tickets:
            show.total_tickets = total_tickets
        if price:
            show.price = price
        if date:
            show.date = date

        try:
            db.session.commit()
            return jsonify({'message': 'Show updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            # Delete the associated bookings with this show
            bookings_to_delete = Booking.query.filter_by(show_id=show_id).all()
            for booking in bookings_to_delete:
                db.session.delete(booking)

            # Delete the show itself
            db.session.delete(show)

            db.session.commit()
            return jsonify({'message': 'Show and associated bookings deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

    elif request.method == 'GET':
        show = Show.query.filter_by(id=show_id).first()
        show_data = {
            "id" : show.id,
            "name" : show.name,
            "tags" : show.tags,
            "rating" : show.rating,
            "theatre_id" : show.theatre_id,
            "total_tickets" : show.total_tickets,
            "price" : show.price,
            "date" : show.date
        }
        return jsonify(show_data) , 200


# # # Theatre search routes
# # @app.route('/theatres/search', methods=['GET'])
# # def search_theatres_by_name():
# #     # Implement logic to search theatres based on theatre name
# #     # Return the list of matching theatres in the response
# #     name = request.args.get('name')
# #     if not name:
# #         return jsonify({'message': 'Theatre name parameter is required'}), 400

# #     # Check if the result is already cached
# #     theatres_cache_key = f"theatres:name:{name}"
# #     cached_theatres = cache.get(theatres_cache_key)
# #     if cached_theatres:
# #         theatres = json.loads(cached_theatres)
# #     else:
# #         theatres = Theatre.query.filter_by(name=name).all()
# #         theatres = [theatre.to_dict() for theatre in theatres]
# #         cache.set(theatres_cache_key, json.dumps(theatres), ex=3600)  # Cache for 1 hour

# #     if not theatres:
# #         return jsonify({'message': 'No theatres found for the given name'}), 404

#     return jsonify({'theatres': theatres}), 200

##### Theatre Search Final Working########
# @app.route('/theatres/search', methods=['GET'])
# @jwt_required()
# def search_theatres():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'message': 'Theatre name parameter is required'}), 400

#     theatres = Theatre.query.filter(Theatre.name.ilike(f'%{name}%')).all()
#     theatres_list = [{'id': theatre.id, 'name': theatre.name, 'place': theatre.place} for theatre in theatres]

#     if not theatres_list:
#         return jsonify({'message': 'No theatres found for the given name'}), 404

#     return jsonify({'theatres': theatres_list}), 200

# #### Final THEATRE SEARCH
# @app.route('/theatres/search', methods=['GET'])
# @jwt_required()
# def search_theatres():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'message': 'Theatre name parameter is required'}), 400

#     # Try to fetch data from cache
#     cached_result = cache.get(name)
#     if cached_result:
#         theatres_list = json.loads(cached_result)  # Load cached data as JSON
#     else:
#         theatres = Theatre.query.filter(Theatre.name.ilike(f'%{name}%')).all()
#         theatres_list = [{'id': theatre.id, 'name': theatre.name, 'place': theatre.place} for theatre in theatres]

#         # Store the data in cache for 1 hour (you can adjust the expiration time)
#         cache.setex(name, 3600, json.dumps({'theatres': theatres_list}))  # Use json.dumps()

#     if not theatres_list:
#         return jsonify({'message': 'No theatres found for the given name'}), 404

#     return jsonify({'theatres': theatres_list}), 200

# @app.route('/theatres/search', methods=['GET'])
# # @jwt_required()
# def search_theatres():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'message': 'Theatre name parameter is required'}), 400

#     print("Checking cache for data:", name)

#     # Try to fetch data from cache
#     cached_result = cache.get(name)
#     if cached_result:
#         print("Data found in cache.")
#         theatres_list = json.loads(cached_result)  # Load cached data as JSON
#     else:
#         print("Data not found in cache. Fetching from the database.")
#         theatres = Theatre.query.filter(Theatre.name.ilike(f'%{name}%')).all()
#         theatres_list = [{'id': theatre.id, 'name': theatre.name, 'place': theatre.place} for theatre in theatres]

#         # Store the data in cache for 1 hour (you can adjust the expiration time)
#         cache.setex(name, 3600, json.dumps({'theatres': theatres_list}))  # Use json.dumps()

#     if not theatres_list:
#         return jsonify({'message': 'No theatres found for the given name'}), 404

#     return jsonify({'theatres': theatres_list}), 200

@app.route('/theatres/search', methods=['GET'])
@jwt_required()
def search_theatres():
    name = request.args.get('name')
    if not name:
        return jsonify({'message': 'Theatre name parameter is required'}), 400

    print("Fetching data from the database.")
    
    theatres = Theatre.query.filter(Theatre.name.ilike(f'%{name}%')).all()
    theatres_list = [{'id': theatre.id, 'name': theatre.name, 'place': theatre.place} for theatre in theatres]

    if not theatres_list:
        return jsonify({'message': 'No theatres found for the given name'}), 404

    return jsonify({'theatres': theatres_list}), 200


# @app.route('/shows/search', methods=['GET'])
# def search_shows():
#     # Implement logic to search shows based on tags, rating, etc.
#     # Return the list of matching shows in the response
#     tags = request.args.get('tags')
#     rating = request.args.get('rating')

#     shows_cache_key = f"shows:{tags}:{rating}"
#     cached_shows = cache.get(shows_cache_key)
#     if cached_shows:
#         shows = json.loads(cached_shows)
#     else:
#         shows = Show.query
#         if tags:
#             shows = shows.filter(Show.tags.contains(tags))
#         if rating:
#             shows = shows.filter_by(rating=rating)
#         shows = shows.all()
#         shows = [show.to_dict() for show in shows]
#         cache.set(shows_cache_key, json.dumps(shows), ex=3600)  # Cache for 1 hour

#     if not shows:
#         return jsonify({'message': 'No shows found for the given criteria'}), 404

    # return jsonify({'shows': shows}), 200

# @app.route('/shows/search', methods=['GET'])
# def search_shows():
#     #name = request.args.get('name')
#     data = request.get_json()
#     name = data.get(name)
#     if not name:
#         return jsonify({'message': 'Show name parameter is required'}), 400

#     shows = Show.query.filter(Show.name.ilike(f'%{name}%')).all()
#     shows_list = [{'id': show.id, 'name': show.name, 'tags': show.tags, 'rating': show.rating} for show in shows]

#     if not shows_list:
#         return jsonify({'message': 'No shows found for the given name'}), 404

#     return jsonify({'shows': shows_list}), 200

###### SHOW SEARCH FINAL CODE #####
# @app.route('/shows/search', methods=['GET'])
# def search_shows():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'message': 'Show name parameter is required'}), 400

#     shows = Show.query.filter(Show.name.ilike(f'%{name}%')).all()
#     print(shows)
#     shows_list = [{'id': show.id, 'name': show.name, 'tags': show.tags, 'rating': show.rating} for show in shows]

#     if not shows_list:
#         return jsonify({'message': 'No shows found for the given name'}), 404

#     return jsonify({'shows': shows_list}), 200

# @app.route('/shows/search', methods=['GET'])
# @jwt_required()
# def search_shows():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'message': 'Show name parameter is required'}), 400

#     # Try to fetch data from cache
#     cached_result = cache.get(name)
#     if cached_result:
#         shows_list = json.loads(cached_result)  # Load cached data as JSON
#     else:
#         shows = Show.query.filter(Show.name.ilike(f'%{name}%')).all()
#         shows_list = [{'id': show.id, 'name': show.name, 'tags': show.tags, 'rating': show.rating} for show in shows]

#         # Store the data in cache for 1 hour (you can adjust the expiration time)
#         cache.setex(name, 3600, json.dumps({'shows': shows_list}))  # Use json.dumps()

#     if not shows_list:
#         return jsonify({'message': 'No shows found for the given name'}), 404

#     return jsonify({'shows': shows_list}), 200
@app.route('/shows/search', methods=['GET'])
@jwt_required()
def search_shows():
    name = request.args.get('name')
    if not name:
        return jsonify({'message': 'Show name parameter is required'}), 400

    shows = Show.query.filter(Show.name.ilike(f'%{name}%')).all()
    shows_list = [{'id': show.id, 'name': show.name, 'tags': show.tags, 'rating': show.rating} for show in shows]

    if not shows_list:
        return jsonify({'message': 'No shows found for the given name'}), 404

    return jsonify({'shows': shows_list}), 200


# Book show tickets route
@app.route('/bookings', methods=['POST'])
@jwt_required()
def book_tickets():
    data = request.get_json()
    # Extract required data from the request and create a new booking
    user_id = get_jwt_identity()
    show_id = data.get('show_id')
    num_tickets = data.get('num_tickets')

    if not show_id or not num_tickets:
        return jsonify({'message': 'Show ID and number of tickets are required'}), 400

    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show not found'}), 404

    if show.total_tickets < num_tickets:
        return jsonify({'message': 'Not enough tickets available for booking'}), 400

    try:
        booking = Booking(user_id=user_id, show_id=show_id, num_tickets=num_tickets, amount=show.price * num_tickets, booking_date=datetime.utcnow())
        db.session.add(booking)
        db.session.commit()

        show.total_tickets -= num_tickets
        db.session.commit()

        return jsonify({'message': 'Booking successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

# Admin view bookings route
# @app.route('/admin-booking', methods=['GET'])
# @cache.cached(timeout=3600)
# #@jwt_required()
# def admin_view_bookings():
#     try:
#         # Get all bookings with associated show and user details
#         # bookings = db.session.query(Booking, Show, User).join(Show).join(User).all()
#         bookings = db.session.query(Booking).all()
#         # print(bookings)
#         # Transform the data for frontend display
#         bookings_list = [{
#             'id': booking.id,
#             'user_id': booking.user.id,
#             'show': {
#                 'name': show.name,
#                 'id': show.id
#             },
#             'num_tickets': booking.num_tickets,
#             'amount': booking.amount
#         } for booking, show, user in bookings]

#         return jsonify(bookings_list), 200
#     except Exception as e:
#         return jsonify({'message': 'Error fetching bookings', 'error': str(e)}), 500

@app.route('/admin-booking', methods=['GET'])
#@cache.cached(timeout=3600)
#@jwt_required()
def admin_view_bookings():
    try:
        # Get all bookings with associated show details
        bookings = db.session.query(Booking, Show).join(Show).all()

        # Transform the data for frontend display
        bookings_list = []
        for booking, show in bookings:
            booking_data = {
                'id': booking.id,
                'show': {
                    'name': show.name,
                    'id': show.id
                },
                'num_tickets': booking.num_tickets,
                'amount': booking.amount
            }
            bookings_list.append(booking_data)

        return jsonify(bookings_list), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching bookings', 'error': str(e)}), 500


# @app.route('/view-user-bookings', methods=['GET'])
# @cache.cached(timeout=3600)
# @jwt_required()
# def view_user_bookings():
#     user_id = get_jwt_identity()
#     bookings = Booking.query.filter_by(user_id=user_id).all()
#     if bookings:
#         booking_info = []
#         for booking in bookings:
#             show = Show.query.get(booking.show_id)
#             booking_data = {
#                 "id": booking.id,
#                 "show_name": show.name,
#                 "show_date": show.date,
#                 "num_tickets": booking.num_tickets,
#                 "amount": booking.amount
#             }
#             booking_info.append(booking_data)

#     return jsonify(booking_info), 200

@app.route('/view-user-bookings', methods=['GET'])
#@cache.cached(timeout=3600)
@jwt_required()
def view_user_bookings():
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    booking_info = []
    
    for booking in bookings:
        show = Show.query.get(booking.show_id)
        
        if show:  # Check if the show exists before accessing its attributes
            booking_data = {
                "id": booking.id,
                "show_name": show.name,
                "show_date": show.date,
                "num_tickets": booking.num_tickets,
                "amount": booking.amount
            }
            booking_info.append(booking_data)
    
    return jsonify(booking_info), 200


# # Export theatre data as CSV route
# @app.route('/export/theatre/<int:theatre_id>/csv', methods=['GET'])
# @jwt_required()
# def export_theatre_data_as_csv(theatre_id):
#     if not g.user.is_admin:
#         return jsonify({'message': 'Only admin can export theatre data as CSV'}), 403

#     theatre = Theatre.query.get(theatre_id)
#     if not theatre:
#         return jsonify({'message': 'Theatre not found'}), 404

#     # Implement logic to export theatre data as CSV for the given theatre_id
#     # ...

#@app.route('/theatre-export/<int:theatre_id>', methods=['GET'])
#@jwt_required
# def random(theatre_id):
#     export_theatre_data_to_csv(theatre_id)
#     if export_theatre_data_to_csv(theatre_id):
#         return "Task Working Successfully"
#     else:
#         return "Task Failed"
    

# @app.route('/theatre-export/<int:theatre_id>', methods=['GET'])
# #@jwt_required
# # def random(theatre_id):
# #     export_theatre_data_to_csv(theatre_id)
# #     if export_theatre_data_to_csv(theatre_id):
# #         return "Task Working Successfully"
# #     else:
# #         return "Task Failed"
    

# #@celery.task
# def export_theatre_data_to_csv(theatre_id):
#     # Fetch the theatre data from the database using the provided theatre_id
#     theatre = Theatre.query.get(theatre_id)

#     if not theatre:
#         return jsonify({'message': 'Theatre not found'}), 404

#     # Calculate the number of shows for the theatre
#     number_of_shows = len(theatre.shows)

#     # Calculate the number of bookings for the theatre
#     number_of_bookings = Booking.query.join(Show).filter(Show.theatre_id == theatre.id).count()

#     # Calculate the average rating for the theatre's shows
#     total_rating = 0
#     num_shows_with_rating = 0
#     for show in theatre.shows:
#         if show.rating is not None:
#             total_rating += show.rating
#             num_shows_with_rating += 1

#     if num_shows_with_rating > 0:
#         average_rating = total_rating / num_shows_with_rating
#     else:
#         average_rating = 0

#     # Prepare the data for CSV export
#     theatre_data = {
#         "id": theatre.id,
#         "name": theatre.name,
#         "place": theatre.place,
#         "capacity": theatre.capacity,
#         "number_of_shows": number_of_shows,
#         "number_of_bookings": number_of_bookings,
#         "average_rating": average_rating,
#     }

#     # Create an in-memory file-like object for writing CSV data
#     csv_buffer = io.StringIO()
    
#     # Use the csv module to create a CSV writer and write the data to the buffer
#     writer = csv.DictWriter(csv_buffer, fieldnames=theatre_data.keys())
#     writer.writeheader()
#     writer.writerow(theatre_data)

#     # Set the response headers to indicate that it's a CSV file
#     response = Response(csv_buffer.getvalue(), content_type='text/csv')
#     response.headers["Content-Disposition"] = f"attachment; filename=theatre_{theatre.name}.csv"

#     return response

#### WORKING

# # Theatre export task
# @celery.task
# #@jwt_required()
# def export_theatre_data_to_csv(theatre_id):
#     with app.app_context():
#         print("OK")
#         theatre = Theatre.query.get(theatre_id)

#         if not theatre:
#             return jsonify({'message': 'Theatre not found'}), 404

#         number_of_shows = len(theatre.shows)
#         number_of_bookings = Booking.query.join(Show).filter(Show.theatre_id == theatre.id).count()

#         total_rating = 0
#         num_shows_with_rating = 0
#         for show in theatre.shows:
#             if show.rating is not None:
#                 total_rating += show.rating
#                 num_shows_with_rating += 1

#         if num_shows_with_rating > 0:
#             average_rating = total_rating / num_shows_with_rating
#         else:
#             average_rating = 0

#         theatre_data = {
#             "id": theatre.id,
#             "name": theatre.name,
#             "place": theatre.place,
#             "capacity": theatre.capacity,
#             "number_of_shows": number_of_shows,
#             "number_of_bookings": number_of_bookings,
#             "average_rating": average_rating,
#         }

#         # Create an in-memory file-like object for writing CSV data
#         csv_buffer = io.StringIO()

#         # Use the csv module to create a CSV writer and write the data to the buffer
#         writer = csv.DictWriter(csv_buffer, fieldnames=theatre_data.keys())
#         writer.writeheader()
#         writer.writerow(theatre_data)

#         csv_data = csv_buffer.getvalue()

#         # Set the response headers to indicate that it's a CSV file
#         response = Response(csv_data, content_type='text/csv')
#         response.headers["Content-Disposition"] = f"attachment; filename=theatre_{theatre.name}.csv"

#         return response

@celery.task
def export_theatre_data_to_csv(theatre_id):
    with app.app_context():
        print("OK")
        theatre = Theatre.query.get(theatre_id)

        if not theatre:
            return {'error': 'Theatre not found'}, 404

        number_of_shows = len(theatre.shows)
        number_of_bookings = Booking.query.join(Show).filter(Show.theatre_id == theatre.id).count()

        total_rating = 0
        num_shows_with_rating = 0
        for show in theatre.shows:
            if show.rating is not None:
                total_rating += show.rating
                num_shows_with_rating += 1

        if num_shows_with_rating > 0:
            average_rating = total_rating / num_shows_with_rating
        else:
            average_rating = 0

        theatre_data = {
            "id": theatre.id,
            "name": theatre.name,
            "place": theatre.place,
            "capacity": theatre.capacity,
            "number_of_shows": number_of_shows,
            "number_of_bookings": number_of_bookings,
            "average_rating": average_rating,
        }

        # Create an in-memory file-like object for writing CSV data
        csv_buffer = io.StringIO()

        # Use the csv module to create a CSV writer and write the data to the buffer
        writer = csv.DictWriter(csv_buffer, fieldnames=theatre_data.keys())
        writer.writeheader()
        writer.writerow(theatre_data)

        csv_data = csv_buffer.getvalue()

        return csv_data  # Return CSV data as the result

# Theatre export route
@app.route('/theatre-export/<int:theatre_id>', methods=['GET'])

#@token_required  # Use your authentication decorator
def initiate_theatre_export(theatre_id):
    task = export_theatre_data_to_csv.apply_async(args=[theatre_id])
    task_id = task.id

    csv_data = task.get()  # Get the CSV data from the Celery task

    response = Response(csv_data, content_type='text/csv')
    theatre = Theatre.query.get(theatre_id)
    response.headers["Content-Disposition"] = f"attachment; filename=theatre_{theatre.name}.csv"

    return response

# # Theatre export route
# @app.route('/theatre-export/<int:theatre_id>', methods=['GET'])
# #@jwt_required()
# #@token_required  # Use your authentication decorator
# def initiate_theatre_export(theatre_id):
#     task = export_theatre_data_to_csv.apply_async(args=[theatre_id])
#     task_id = task.id

#     return export_theatre_data_to_csv(theatre_id)

# # Theatre export task
# @celery.task
# #@jwt_required()
# def export_theatre_data_to_csv(theatre_id):
#     with app.app_context():
#         print("OK")
#         theatre = Theatre.query.get(theatre_id)

#         if not theatre:
#             return {'error': 'Theatre not found'}, 404

#         number_of_shows = len(theatre.shows)
#         number_of_bookings = Booking.query.join(Show).filter(Show.theatre_id == theatre.id).count()

#         total_rating = 0
#         num_shows_with_rating = 0
#         for show in theatre.shows:
#             if show.rating is not None:
#                 total_rating += show.rating
#                 num_shows_with_rating += 1

#         if num_shows_with_rating > 0:
#             average_rating = total_rating / num_shows_with_rating
#         else:
#             average_rating = 0

#         theatre_data = {
#             "id": theatre.id,
#             "name": theatre.name,
#             "place": theatre.place,
#             "capacity": theatre.capacity,
#             "number_of_shows": number_of_shows,
#             "number_of_bookings": number_of_bookings,
#             "average_rating": average_rating,
#         }

#         # Create an in-memory file-like object for writing CSV data
#         csv_buffer = io.StringIO()

#         # Use the csv module to create a CSV writer and write the data to the buffer
#         writer = csv.DictWriter(csv_buffer, fieldnames=theatre_data.keys())
#         writer.writeheader()
#         writer.writerow(theatre_data)

#         csv_data = csv_buffer.getvalue()

#         return csv_data

# # Theatre export route
# @app.route('/theatre-export/<int:theatre_id>', methods=['GET'])
# #@jwt_required()
# #@token_required  # Use your authentication decorator
# def initiate_theatre_export(theatre_id):
#     task = export_theatre_data_to_csv.apply_async(args=[theatre_id])
#     task_id = task.id

#     csv_data = task.get()  # Get the CSV data from the Celery task

#     response = Response(csv_data, content_type='text/csv')
#     response.headers["Content-Disposition"] = f"attachment; filename=theatre_{theatre.name}.csv"

#     return response


# # Export show data as CSV route
# @app.route('/export/show/<int:show_id>/csv', methods=['GET'])
# @jwt_required()
# def export_show_data_as_csv(show_id):
#     if not g.user.is_admin:
#         return jsonify({'message': 'Only admin can export show data as CSV'}), 403

#     show = Show.query.get(show_id)
#     if not show:
#         return jsonify({'message': 'Show not found'}), 404

#     # Implement logic to export show data as CSV for the given show_id
#     # ...

# Export theatre data as CSV route
# @app.route('/export/theatre/<int:theatre_id>/csv', methods=['GET'])
# @jwt_required()
# def export_theatre_data_as_csv(theatre_id):
#     if not g.user.is_admin:
#         return jsonify({'message': 'Only admin can export theatre data as CSV'}), 403

#     theatre = Theatre.query.get(theatre_id)
#     return export_theatre_data_to_csv(theatre)


# # Daily reminder job route
# @app.route('/schedule/daily-reminder', methods=['POST'])
# #@jwt_required()
# def schedule_daily_reminder():
#     user_id = 1 #get_jwt_identity()
#     send_daily_reminder.apply_async(args=[user_id])  # Example: Send reminder after 10 seconds
#     #send_daily_reminder(user_id)
#     #print(user_id)
#     return jsonify({'message': 'Daily reminder job scheduled'}), 200
    
# @celery.task
# def send_daily_reminder(user_id):
#     print("OK")
#     # user = User.query.get(user_id)
#     # # Check if the user has not visited/booked anything
#     # # Your logic to check if the user has not visited/booked anything
#     # # For example:
#     # bookings = Booking.query.filter_by(user_id=user_id).all()
#     # if not bookings:
#     #     # If the user has not booked anything, send a reminder email
#     #     subject = "Daily Reminder - Visit/Book Entertainment"
#     #     body = f"Hello {user.username},\n\nThis is a friendly reminder to visit/book entertainment today.\n\nBest regards,\nYour Entertainment Team"
#     #     send_email(user.email, subject, body)
#     # else:
#     #     # If the user has already booked, no need to send a reminder
#     #     pass

# def send_email(to, subject, body):
#     # Helper function to send email using Flask-Mail
#     msg = Message(subject, recipients=[to], body=body)
#     mail.send(msg)


@app.route('/schedule/daily-reminder', methods=['POST'])
def schedule_daily_reminder():
    #user_id = request.json.get('user_id')

    # if not user_id:
    #     return jsonify({'error': 'User ID required'}), 400

    send_daily_reminder.apply_async()
    return jsonify({'message': 'Daily reminder scheduled'}), 200

# @celery.task()
# def send_daily_reminder():
#     with app.app_context():
#         users = User.query.all()
#         for user in users:
#             if user:
#                 today = datetime.today().date()
#                 bookings_today = Booking.query.filter_by(user_id=user.id, booking_date=today).all()

#                 if not bookings_today:
#                     subject = "Your Daily Reminder"
#                     body = f"Hi {user.username}, this is your daily reminder to book a show!"
#                     try:
#                         msg = Message(subject=subject, recipients=[user.email], body=body)
#                         mail.send(msg)
#                         # print(f"Email sent to {user.email} successfully")
#                     except Exception as e:
#                         # print(f"Error sending email to {user.email}: {str(e)}")
#                         pass

@celery.task()
def send_daily_reminder():
    with app.app_context():
        today = datetime.utcnow().date()
        deadline_time = datetime(today.year, today.month, today.day, 6, 0, 0)  # 18:00 (6:00 PM) UTC

        users = User.query.all()

        for user in users:
            bookings_today = Booking.query.filter_by(user_id=user.id, booking_date=today).all()

            if not bookings_today and datetime.utcnow() <= deadline_time:
                subject = "Your Daily Reminder"
                body = f"Hi {user.username}, this is your daily reminder to book a show!"
                try:
                    msg = Message(subject=subject, recipients=[user.email], body=body)
                    mail.send(msg)
                except Exception as e:
                    pass
            # Check if user has never booked any tickets (not in Booking table)
            if not user.bookings:
                subject = "Your Daily Reminder"
                body = f"Hi {user.username}, this is your daily reminder to book a show!"
                try:
                    msg = Message(subject=subject, recipients=[user.email], body=body)
                    mail.send(msg)
                except Exception as e:
                    pass



        # subject = "Your Daily Reminder"
        # body = f"Hi , this is your daily reminder to book a show!"
        # #send_email(user.email, subject, body)
        # abc = "xyz@xyz.com"
        # try:
        #     msg = Message(subject=subject, recipients=[abc], body=body)
        #     mail.send(msg)
        #     #print(f"Email sent to {to} successfully")
        # except Exception as e:
        #     #print(f"Error sending email to {to}: {str(e)}")
        #     pass


# @app.route('/schedule/monthly-report', methods=['POST'])
# # @jwt_required()
# def schedule_monthly_report():
#     user_id = get_jwt_identity()  # You can replace this with the actual user ID
#     generate_monthly_report.apply_async(args=[user_id])

#     return jsonify({'message': 'Monthly entertainment report job scheduled'}), 200

@app.route('/schedule/monthly-report', methods=['POST'])
def schedule_monthly_report():
    user_id = 1
    ist = timezone('Asia/Kolkata')
    now = datetime.now(ist)
    send_datetime = ist.localize(datetime(year=now.year, month=now.month, day=13, hour=13, minute=8, second=00))
    
    # users = User.query.all()
    # for user in users:
    #     schedule_monthly_report_task.apply_async(args=[user.id, send_datetime])

    #user_id = 1 #get_jwt_identity()  # You can replace this with the actual user ID
    #now = datetime.now()
    #send_datetime = datetime(year=now.year, month=now.month, day=12, hour=22, minute=56, second=10)
    schedule_monthly_report_task.apply_async(args=[user_id, send_datetime])  # Pass send_datetime directly

    return jsonify({'message': 'Monthly entertainment report job scheduled'}), 200

def generate_report_html(bookings, user):
    # Use a Jinja2 template to generate the HTML report
    template = """
    <html>
    <head>
        <title>Monthly Entertainment Report</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Monthly Entertainment Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Booking ID</th>
                    <th>User</th>
                    <th>Show</th>
                    <th>Date</th>
                    <th>Rating</th>
                </tr>
            </thead>
            <tbody>
                {% for booking in bookings %}
                <tr>
                    <td>{{ booking.id }}</td>
                    <td>{{ booking.user.username }}</td>
                    <td>{{ booking.show.name }}</td>
                    <td>{{ booking.booking_date.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    <td>{{ booking.related_show.rating or 'N/A' }}</td>
                </tr>
                {% endfor %}
                {% if not bookings %}
                <tr>
                    <td colspan="5">You haven't booked anything in this month.</td>
                </tr>
                {% endif %}
            </tbody>
        </table>
    </body>
    </html>
    """

    # Render the template using Jinja2
    report_html = render_template_string(template, bookings=bookings, user=user)

    return report_html

@celery.task
def schedule_monthly_report_task(user_id, send_datetime):
    send_monthly_report.apply_async(eta=send_datetime)


@celery.task
def send_monthly_report():
    with app.app_context():
        admin = Admin.query.first()  # Get the admin user (you might want to change this based on your logic)
        today = datetime.today()
        last_month = today.replace(day=1) - timedelta(days=1)

        users = User.query.all()
        for user in users:
            bookings = Booking.query.filter(
                Booking.user == user,
                Booking.booking_date >= last_month.replace(day=1),
                Booking.booking_date <= today
            ).options(
                db.joinedload(Booking.user),  # Load the user relationship
                db.joinedload(Booking.related_show)  # Load the related_show relationship
            ).all()

            if bookings:
                # Your logic to generate the report in HTML/PDF format
                report = generate_report_html(bookings, user)

                # Send the report as an email to the user
                user_subject = "Monthly Entertainment Report"
                user_body = f"Hello {user.username},\n\nHere is your monthly entertainment report:\n\n{report}\n\nBest regards,\nYour Entertainment Team"
                user_msg = Message(subject=user_subject, recipients=[user.email], html=user_body)
                mail.send(user_msg)

                # Send the report as an email to the admin
                admin_subject = "Monthly Entertainment Report"
                admin_body = f"Hello Admin,\n\nHere is the monthly entertainment report for user {user.username}:\n\n{report}\n\nBest regards,\nYour Entertainment Team"
                admin_msg = Message(subject=admin_subject, recipients=[admin.email], html=admin_body)
                mail.send(admin_msg)
            else:
                # Send a message to the user indicating no bookings for the month
                user_subject = "Monthly Entertainment Report"
                user_body = f"Hello {user.username},\n\nYou haven't booked anything in this month.\n\nBest regards,\nYour Entertainment Team"
                user_msg = Message(subject=user_subject, recipients=[user.email], body=user_body)
                mail.send(user_msg)

# def send_monthly_report(user_id):
#     with app.app_context():
#         user = User.query.get(user_id)
#         admin = Admin.query.first()  # Get the admin user (you might want to change this based on your logic)

#         if user:
#             today = datetime.today()
#             last_month = today.replace(day=1) - timedelta(days=1)
#             bookings = Booking.query.filter(
#                 Booking.booking_date >= last_month.replace(day=1),
#                 Booking.booking_date <= today
#             ).options(
#                 db.joinedload(Booking.user),  # Load the user relationship
#                 db.joinedload(Booking.related_show)  # Load the related_show relationship
#             ).all()

#             # Your logic to generate the report in HTML/PDF format
#             report = generate_report_html(bookings)

#             # Render the report template using Flask's render_template
#             report_rendered = render_template_string(report=report, bookings=bookings)

#             # Send the report as an email to the user
#             user_subject = "Monthly Entertainment Report"
#             user_body = f"Hello {user.username},\n\nHere is your monthly entertainment report:\n\n{report_rendered}\n\nBest regards,\nYour Entertainment Team"
#             user_msg = Message(subject=user_subject, recipients=[user.email], html=user_body)
#             mail.send(user_msg)

#             # Send the report as an email to the admin
#             admin_subject = "Monthly Entertainment Report"
#             admin_body = f"Hello Admin,\n\nHere is the monthly entertainment report for user {user.username}:\n\n{report_rendered}\n\nBest regards,\nYour Entertainment Team"
#             admin_msg = Message(subject=admin_subject, recipients=[admin.email], html=admin_body)
#             mail.send(admin_msg)

# def send_monthly_report(user_id):
#     with app.app_context():
#         user = User.query.get(user_id)
#         admin = Admin.query.first()  # Get the admin user (you might want to change this based on your logic)

#         if user:
#             today = datetime.today()
#             last_month = today.replace(day=1) - timedelta(days=1)
#             bookings = Booking.query.filter(
#                 Booking.booking_date >= last_month.replace(day=1),
#                 Booking.booking_date <= today
#             ).options(
#                 db.joinedload(Booking.user),  # Load the user relationship
#                 db.joinedload(Booking.related_show)  # Load the related_show relationship
#             ).all()

#             # Your logic to generate the report in HTML/PDF format
#             report = generate_report_html(bookings)

#             user_subject = "Monthly Entertainment Report"
#             user_body = f"Hello {user.username},\n\nHere is your monthly entertainment report:\n\n{report}\n\nBest regards,\nYour Entertainment Team"
#             user_msg = Message(subject=user_subject, recipients=[user.email], body=user_body)
#             mail.send(user_msg)

#             # Send the report as an email to the admin
#             admin_subject = "Monthly Entertainment Report"
#             admin_body = f"Hello Admin,\n\nHere is the monthly entertainment report for user {user.username}:\n\n{report}\n\nBest regards,\nYour Entertainment Team"
#             admin_msg = Message(subject=admin_subject, recipients=[admin.email], body=admin_body)
#             mail.send(admin_msg)

# def send_email_to_admin(subject, body):
#     admin_email = "astroninja@skiff.com"  # Replace with your admin's email address
#     msg = Message(subject, recipients=[admin_email], body=body)
#     mail.send(msg)
# @celery.task
# def generate_monthly_report(user_id):
#     # today = datetime.today()
#     # last_month = today.replace(day=1) - timedelta(days=1)
#     # bookings = Booking.query.filter(Booking.date >= last_month, Booking.date <= today).all()
#     today = datetime.today()
#     last_month = today.replace(day=1) - timedelta(days=1)
#     bookings = Booking.query.filter(Booking.date >= last_month.replace(day=1), Booking.date <= today).all()

#     # Your logic to generate the report in HTML/PDF format
#     report = generate_report_html(bookings)

#     # Send the report as an email
#     subject = "Monthly Entertainment Report"
#     body = f"Hello,\n\nHere is the monthly entertainment report:\n\n{report}\n\nBest regards,\nYour Entertainment Team"
#     send_email_to_admin(subject, body)


if __name__ == '__main__':
    app.run(debug=True)
