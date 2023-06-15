import os
from cs50 import SQL
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT-SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

db = SQL("sqlite:///frosh.db")

SPORTS = [
    "Dodgeball",
    "Flag Football",
    "Soccer",
    "Volleyball",
    "Ultimate Frisbee"
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if (sport != None and sport not in SPORTS) or (not name and not sport):
        return render_template("error.html", message="Invalid input")
    elif not name:
        return render_template("error.html", message="Name not typed")
    elif not sport:
        return render_template("error.html", message="Sport not selected")

    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    return render_template("success.html", sport=sport)


@app.route("/see_list", methods=["GET"])
def see_list():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)