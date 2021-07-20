from flask import Flask, render_template, request, Response
import os
import json

# from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# from app.db import get_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
data_file = os.path.join(PROJECT_ROOT, "static/data.json")
data = json.load(open(data_file))
# data_file.close()

# dB
# app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
# db.init_app(app)

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    # TODO: Return a restister page
    # return "Register Page not yet implemented", 5010
    return render_template("register.html", title="Register")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    # TODO: Return a login page

    return render_template("login.html", title="Login")


# Create URL routes
@app.route("/")
def home():
    allUsers = data
    return render_template("home.html", allUsers=allUsers)


# register and login routes for dbsqlite:
# @app.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#        password = request.form.get('password')
#        db = get_db()
#        error = None
#
#        if not username:
#            error = 'Username is required.'
#        elif not password:@@@app.route('/login', methods=('GET', 'POST'))
#            error = 'Password is required.'
#        elif db.execute(
#                 'SELECT id FROM user WHERE username = ?', (username,)
#
# 	        'SELECT id FROM user WHERE username = ?', (username,)
#        ).fetchone() is not None:
#            error = "User {username} is already registered."
#
#        if error is None:
#             db.execute(
#                     'INSERT INTO user (username, password) VALUES (?, ?)',
#
# 	            'INSERT INTO user (username, password) VALUES (?, ?)',
#
#                (username, generate_password_hash(password))
#            )
#            db.commit()
#            return f"User {username} created successfully\n"
#        else:
#            return error, 418
#
#
#    ## TODO: Return a restister page
#    #return "Register Page not yet implemented", 501
#    return render_template("register.html", title="Register")
#
#    ## TODO: Return a restister page
#    #return "Register Page not yet implemented", 501
#    return render_template("register.html")
#
# @app.route('/login', methods=('GET', 'POST'))
# def login():
#    if request.method == 'POST':
#        username = request.form.get('username')
#        password = request.form.get('password')
#        db = get_db()
#        error = None
#        user = db.execute(
#            'SELECT * FROM user WHERE username = ?', (username,)
#        ).fetchone()
#
#        if user is None:
#            error = 'Incorrect username.'
#        elif not check_password_hash(user['password'], password):
#            error = 'Incorrect password.'
#
#        if error is None:
#            return "Login Successful\n", 200
#        else:
#            return error, 418
#
#    ## TODO: Return a login page:
#    #return "Login Page not yet implemented", 501
#    return render_template("login.html", title="Login")
#
#    ## TODO: Return a login page:
#    #return "Login Page not yet implemented", 501
#    return render_template("login.html")


@app.route("/health")
def starting_url():
    status_code = Response(status=200)
    return status_code


# app.run(host="0.0.0.0", port=5000)

# Create URL for each members
@app.route("/about/<string:name>")
def about(name):
    userData = data[name]
    allUsers = data
    return render_template(
        "about.html", name=name, userData=userData, allUsers=allUsers
    )


if __name__ == "__main__":
    # rid (port="5002") within run function
    app.run(debug=True)

    app.run(debug=True)
