# Importing necessary modules
import os
import sqlite3
import cs50

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database and set same thread to false
db = cs50.SQL("sqlite:///userstats.db")
conn = sqlite3.connect('userstats.db', check_same_thread=False)


@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
# This is the home page, no functionality, just the home page.
def index():
    id = session["user_id"]
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Get route
    if request.method == "GET":
        return render_template("register.html")
    # Post route
    else:
        # Get username, password, and password1 AKA confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        user_name = db.execute("SELECT username FROM users WHERE username = ? ", username)
        if not username:
            return apology("must provide username", 400)
        elif not password or not confirmation:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("password doesn't match", 400)
        # Generate hash for password, then ensure there is not a duplicate username
        else:
            hash = generate_password_hash(password)
            try:
                db.execute("INSERT INTO users (username, hash ) VALUES (?,?)", username, hash)
                session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)
                session.clear()
                return render_template("/login.html")
            
            except ValueError:
                return apology("username already exists", 400)

@app.route("/recordshots", methods=["GET", "POST"])
@login_required
# Function to record the shots for the signed in user
def recordshots():
    user_id = session["user_id"]
    try:
        shots = db.execute("SELECT * FROM shots WHERE id = ?", (session["user_id"],))
    except ValueError:
        return apology("SELECT Error", 400)
    if request.method == "GET":
        return render_template("recordshots.html", shots=shots)
    if request.method == "POST":
            # Insert the shot data and id into the database
            db.execute("INSERT INTO shots (id, shotnumber, shot) VALUES (?,?,?)", session["user_id"], request.form.get("shotnumber"), request.form.get("shot"))
            return render_template("recordshots.html", shots=shots)
        
@app.route("/recordgames", methods=["GET", "POST"])
@login_required
# Function to record the games for the signed in user
def recordgames():
    user_id = session["user_id"]
    try:
        games = db.execute("SELECT COUNT(gamenumber) FROM winrecord WHERE id = ?", (session["user_id"],))
    except ValueError:
        return apology("SELECT Error", 400)
    # Get route
    if request.method == "GET":
        return render_template("recordgames.html", games=games)
    # Post route
    if request.method == "POST":
        # Insert the game result and id into the database
        if request.form.get("win"):
            db.execute("INSERT INTO winrecord (id, result) VALUES (?,?)", session["user_id"], request.form.get("win"))
            return render_template("/recordgames.html")
        # Insert the game result and id into the database
        elif request.form.get("loss"):
            db.execute("INSERT INTO winrecord (id, result) VALUES (?,?)", session["user_id"], request.form.get("loss"))
            return render_template("/recordgames.html")

@app.route("/shotrecord", methods=["GET", "POST"])
@login_required
# Function to display the shot record for the signed in user
def shotrecord():
    # Get route
    if request.method == "GET":
        shots = db.execute("SELECT * FROM shots WHERE id = ?", session["user_id"])
        return render_template("shotrecord.html", shots=shots)
    # Post route
    elif request.method == "POST":
        return render_template("shotrecord.html")

@app.route("/gamerecords", methods=["GET", "POST"])
@login_required
# Function to display the game record for the signed in user
def winrecord():
    # Get route
    if request.method == "GET":
        games = db.execute("SELECT * FROM winrecord WHERE id = ?", session["user_id"])
        return render_template("gamerecords.html", games=games)
    # Post route
    elif request.method == "POST":
        return render_template("gamerecords.html")


@app.route("/percentage", methods=["GET", "POST"])
@login_required
def percentage():
    # Function to acquire the neccesaary data to calculate the shooting and win percentage for the signed in user
    shotstaken1 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ?", session["user_id"])))
    shotstaken = shotstaken1[0]["COUNT(shot)"]

    shotsmade1 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "1")))
    shotsmade2 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "2")))
    shotsmade3 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "3")))
    shotsmade4 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "4")))
    shotsmade5 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "5")))
    shotsmade6 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "6")))
    shotsmade7 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "7")))
    shotsmade8 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "8")))
    shotsmade9 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "9")))
    shotsmade10 = ((db.execute("SELECT COUNT(shot) FROM shots WHERE id = ? AND shot = ?", session["user_id"], "10")))

    # Converting list to int
    shotsmade = int(shotsmade1[0]["COUNT(shot)"] + shotsmade2[0]["COUNT(shot)"] + shotsmade3[0]["COUNT(shot)"] + shotsmade4[0]["COUNT(shot)"] + shotsmade5[0]["COUNT(shot)"] + shotsmade6[0]["COUNT(shot)"] + shotsmade7[0]["COUNT(shot)"] + shotsmade8[0]["COUNT(shot)"] + shotsmade9[0]["COUNT(shot)"] + shotsmade10[0]["COUNT(shot)"])
    shotsmissed = int(shotstaken - shotsmade)

    # Calculating the shooting percentage
    if shotstaken == 0:
        percentage = 0
    else:
        percentage = round(shotsmade / shotstaken, 4) * 100

    gamesplayed1 = (db.execute("SELECT COUNT(gamenumber) FROM winrecord WHERE id = ?", session["user_id"]))
    gameswon1 = (db.execute("SELECT COUNT(result) FROM winrecord WHERE id = ? AND result = ?", session["user_id"], "Win"))
    gameslost1 = (db.execute("SELECT COUNT(result) FROM winrecord WHERE id = ? AND result = ?", session["user_id"], "Loss"))

    # Converting list to int
    gamesplayed = int(gamesplayed1[0]["COUNT(gamenumber)"])
    gameswon = int(gameswon1[0]["COUNT(result)"])
    gameslost = int(gameslost1[0]["COUNT(result)"])

    # Calculating the win percentage
    if gamesplayed == 0:
        winpercentage = 0
    else:
        winpercentage = round(gameswon / gamesplayed, 4) * 100

    return  render_template("percentage.html", 
                            percentage=percentage, shotsmade=shotsmade, shotstaken=shotstaken, shotsmissed=shotsmissed, gamesplayed=gamesplayed, gameswon=gameswon, gameslost=gameslost, winpercentage=winpercentage)








    


