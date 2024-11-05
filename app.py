from flask import Flask, render_template, request, redirect, session
from db import db_init, add_user, get_users, get_user, delete_user
from middlware import auth_middlware

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Initialize the database when the app starts
with app.app_context():
    db_init()

SPORTS = [
    "football",
    "soccer",
    "volleyball"
]


@app.route("/")
@auth_middlware
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
    # check if the name already exists
    existed_user = get_user(name)
    if existed_user:
        return render_template("error.html", error="name already exists try using another")
    # store the user data
    add_user(name, password, sport)
    return redirect("/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if not name or not password:
            return render_template("error.html", error="name feild is required")
        # get the user
        user = get_user(name)
        if not user:
            print("user not found")
            return render_template("error.html", error="incorrect name or password")
        # validate the password
        if not user[2] == password:
            print("passwords dont match")
            return render_template("error.html", error="password incorrect")
        # store the session
        print("storing the session")
        session["name"] = user[1]
        session["id"] = user[0]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/users")
def users_list():
    users = get_users()
    return render_template("user_list.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if not id:
        return render_template("error.html", error="Id not provided correctly")
    session.clear()
    delete_user(id)
    return redirect("/register")


if __name__ == "__main__":
    app.run()