from flask import Flask, render_template, request
from db import db_init, add_user

app = Flask(__name__)

# Initialize the database when the app starts
with app.app_context():
    db_init()

SPORTS = [
    "football",
    "soccer",
    "volleyball"
]

@app.route("/")
def index ():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register ():
    if request.method == "GET":
        return render_template("register.html")
    
    name = request.form.get("name")
    password = request.form.get("password")
    sport = request.form.get("sport")

    if sport not in SPORTS:
        return render_template("error.html", error="the sport you choose is not available")
    if not name or not password or not sport:
        return render_template("error.html", error="All fields are required")
    
    # store the user data
    query = "INSERT INTO users(name, password, sport) VALUES (?, ?, ?)"
    add_user(query, (name, password, sport))
    
    return render_template("success.html", message="User Registered")




@app.route("/users")
def users_list():
    return render_template("user_list.html")
