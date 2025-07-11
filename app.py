from flask import Flask, render_template, request, redirect, session, url_for, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from helpers import *

app = Flask(__name__)
app.secret_key = "a4f812f0348b429aaea133f5db7848f1"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db:
        db.close()

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm  = request.form["confirm"]

        if not username or not password or password != confirm:
            flash("Invalid input.")
            return redirect(url_for("register"))

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username already taken.")
            return redirect(url_for("register"))

        flash("Registered! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        row = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            session.clear()
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            return redirect(url_for("index"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        city = request.form.get("city")
        keyword = request.form.get("keyword")
        events = get_events(city, keyword)
        return render_template("results.html", events=events)
    return render_template("index.html")

@app.route("/results")
@login_required
def results():
    city    = request.args.get("city")
    keyword = request.args.get("keyword")
    events  = []  # <- call your Ticketmaster helper here
    return render_template("results.html", events=events, city=city, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)