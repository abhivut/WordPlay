import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from random import choice

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///vocab.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

p = ""
set = ""

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    """Homepage"""
    p = ""

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if request.method == 'POST':

        sets = db.execute("SELECT * FROM sets WHERE setName = ? AND id = ?  AND word <> '*'", request.form.get("display"), session["user_id"])
        sets2 = db.execute("SELECT DISTINCT * FROM sets WHERE setName = ? AND id = ? AND word <> '*'", request.form.get("display"), session["user_id"])
        Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        len1 = len(sets2)
        len2 = len(sets)
        view = "visible"

        if len(Dsets) == 0:
            return render_template("index.html", len = len1, user = user[0]["username"], view = view, hiddenN = "visible")

        if request.form.get("display") == "View All":
            sets = db.execute("SELECT * FROM sets WHERE id = ? AND word <> '*'", session["user_id"])
            Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
            len2 = len(sets)

            return render_template("index.html", sets = sets, Dsets = Dsets, len = len1, len2 = len2, user = user[0]["username"], view = view, hiddenN = "hidden")

        return render_template("index.html", sets = sets, Dsets = Dsets, len = len1, len2 = len2, user = user[0]["username"], view = view, hiddenN = "hidden")

    else:

        Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        len1 = len(Dsets)
        view = "hidden"
        if len1 == 0:
            return render_template("index.html", len = len1, user = user[0]["username"], view = view, hiddenN = "visible")
        return render_template("index.html", Dsets = Dsets, len = len1, user = user[0]["username"], view = view, hiddenN = "hidden")

@app.route("/learn", methods=["GET", "POST"])
@login_required
def study():
    """Study your sets"""
    if request.method == 'POST':
        Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        sets = db.execute("SELECT * FROM sets WHERE id = ? AND setName = ? AND word <> '*'", session["user_id"], request.form.get("display"))
        return render_template("learn.html", Dsets = Dsets, sets = sets)
    else:
        Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        sets = db.execute("SELECT * FROM sets WHERE id = ?", session["user_id"])
        return render_template("learn.html", Dsets = Dsets)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Define P
    p = ""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            p = "Please enter a username!"
            return render_template("login.html", p = p)

        # Ensure password was submitted
        elif not request.form.get("password"):
            p = "Please enter a password!"
            return render_template("login.html", p = p)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            p = "Invalid username and/or password!"
            return render_template("login.html", p = p)

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


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Get sword definition"""
    sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
    if request.method == 'POST':
        global word
        word = request.form.get("word")
        if not request.form.get("word"):
            p = "Please enter a word :("
            word = ""
            return render_template("search.html", hidden = 'hidden', p = p, sets = sets)
        definition = lookup(request.form.get("word"))
        if definition == None:
            word = ""
            return render_template("search.html", hidden = 'hidden', p = "Word isn't in dictionary :(", sets = sets)

        return render_template("search.html", definition = definition["definition"], word = request.form.get("word"), hidden = 'visible', sets = sets)
    else:

        return render_template("search.html", hidden = 'hidden', sets = sets)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        hash = generate_password_hash(request.form.get("password"))

        # Check for username
        if not request.form.get("username"):
            p = "Please enter a username!"
            return render_template("register.html", p = p)

        # Check if username already in database
        elif len(rows) == 1:
            p = "Username already exists!"
            return render_template("register.html", p = p)

        # Username must be 3 characters
        elif len(request.form.get("username")) < 3:
            p = "Username must be at least 3 characters!"
            return render_template("register.html", p = p)

        # Password must be 3 characters
        elif len(request.form.get("password")) < 3:
            p = "Password must be at least 3 characters!"
            return render_template("register.html", p = p)

        # Check for password
        elif not request.form.get("password"):
            p = "Please enter password!"
            return render_template("register.html", p = p)

        # Check for confirmation of password
        elif not request.form.get("confirmation"):
            p = "Please confirm password!"
            return render_template("register.html", p = p)

        # Check if both passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            p = "Passwords do not match!"
            return render_template("register.html", p = p)

        # Insert into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)

        # Redefine rows
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Start session
        session["user_id"] = rows[0]["id"]

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create sets"""
    p = ""

    sets = db.execute("SELECT * FROM sets WHERE setName = ? AND id = ?", session["user_id"], request.form.get("set"))

    if request.method == 'POST':
        if not request.form.get("set"):
            p = "Set not entered!"
            return render_template("create.html", p = p)

        if len(sets) > 0:
            p = "Set already exists!"
            return render_template("create.html", p = p)

        db.execute("INSERT INTO sets (id, setName, word, definition) VALUES (?, ?, ?, ?)", session["user_id"], request.form.get("set"), '*', '*')

        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add words"""
    p = ""
    sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
    if request.method == 'POST':
        
            if not request.form.get("word"):
                p = "Word not found!"
                return render_template("add.html", p = p, sets = sets)

            if not request.form.get("definition"):
                p = "Definition not found!"
                return render_template("add.html", p = p, sets = sets)

            if not request.form.get("set"):
                p = "Set not entered!"
                return render_template("add.html", p = p, sets = sets)

            db.execute("INSERT INTO sets (id, setName, word, definition) VALUES (?, ?, ?, ?)", session["user_id"], request.form.get("set"), request.form.get("word"), request.form.get("definition"))

            return redirect("/")
    else:
        sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        if len(sets) == 0:
            return redirect("/create")

        return render_template("add.html", sets = sets)

@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
    if request.method == "POST":
        global set
        set = request.form.get("set")
        sets = db.execute("SELECT * FROM sets WHERE id = ? AND setName = ?  AND word <> '*'", session["user_id"], set)
        if len(sets) == 0:
            return render_template("tested.html", sets = sets, hidden = 'hidden', hiddenF = 'hidden')
        return render_template("tested.html", sets = sets, hidden = 'hidden', hiddenF = 'visible')
    else:
        Dsets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
        return render_template("test.html", Dsets = Dsets)


@app.route("/tested", methods=["GET", "POST"])
@login_required
def tested():
    if request.method == 'POST':
        i = 0
        wrong = []
        sets = db.execute("SELECT * FROM sets WHERE id = ? AND setName = ? AND word <> '*'", session["user_id"], set)
        for seta in sets:
            if seta["word"].lower() == request.form.get(seta["word"]).lower():
                i += 1
            else:
                wrong.append(seta["word"])
        len1 = len(sets)
        len1 = str(len1)
        score = str(i) + "/" + len1
        if wrong == []:
            wrong = ['None!']
        return render_template("tested.html", score = score, hidden = 'visible', hiddenF = 'hidden', wrong = wrong)

@app.route("/deleteW", methods=["GET", "POST"])
@login_required
def deleteW():
    sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
    setsL = db.execute("SELECT * FROM sets WHERE id = ? AND setName = ? AND word = ?", session["user_id"], request.form.get("set"), request.form.get("word"))
    if request.method == 'POST':
        if not request.form.get("word"):
            p = "Word missing!"
            return render_template("deleteW.html", p = p, sets = sets)
        if len(setsL) == 0:
            p = "Word doesn't exist!"
            return render_template("deleteW.html", p = p, sets = sets)

        db.execute("DELETE FROM sets WHERE id = ? AND setName = ? AND word = ?", session["user_id"], request.form.get("set"), request.form.get("word"))
        return redirect("/")
    else:
        return render_template("deleteW.html", sets = sets)

@app.route("/deleteS", methods=["GET", "POST"])
@login_required
def deleteS():
    sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
    if request.method == 'POST':
        db.execute("DELETE FROM sets WHERE id = ? AND setName = ?", session["user_id"], request.form.get("set"))
        return redirect("/")
    else:
        return render_template("deleteS.html", sets = sets)

@app.route("/addS", methods=["GET", "POST"])
@login_required
def addS():
    p = ""
    sets = db.execute("SELECT DISTINCT setName FROM sets WHERE id = ?", session["user_id"])
    if request.method == 'POST':
        if word == "":
            p = "Word is invalid!"
            return render_template("search.html", p = p, sets = sets)
        db.execute("INSERT INTO sets (id, setName, word, definition) VALUES (?, ?, ?, ?)", session["user_id"], request.form.get("set"), word, lookup(word)["definition"])
        return redirect("/")
    else:
        return render_template("deleteS.html", sets = sets)