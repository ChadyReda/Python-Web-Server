from flask import Flask, render_template, request, redirect
from db import db_init, add_user, get_users, delete_user

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
    add_user(name, password, sport)
    return redirect("/")


@app.route("/users")
def users_list():
    users = get_users()
    return render_template("user_list.html", users=users)


@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if not id:
        return render_template("error.html", message="No id is provided")
    delete_user(id)
    return redirect("/register")