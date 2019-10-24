import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register_page")
def register_page():
    return render_template("register.html")


@app.route("/registration", methods=["POST"])
def registration():
    # grab user's info from the form
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)  # hash the password

    # insert user's info into the database
    db.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (:first_name, :last_name, :username, :password)", {"first_name": first_name, "last_name": last_name, "username": username, "password": hashed_password})
    db.commit()  # finalize the transaction

    return render_template("success.html", foo="registered", username=username)


if __name__ == "__main__":
    app.run()

