import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, usd
from werkzeug.security import check_password_hash, generate_password_hash

# Configure Application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in

    # Forget any user_id
    session.clear()

    # Initialize database
    database = sqlite3.connect("users.db")
    db = database.cursor()  

    # POST
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        # Check if username was submitted
        if not name:
            database.close()
            return redirect("#")            
        
        # Check if password was submitted
        if not password:
            database.close()
            return redirect("#")            

        # Get user info from database
        db.execute("""SELECT * FROM users WHERE username=?""", (name,))     
        user_info= db.fetchall()          

        # Check for valid username and password
        if len(user_info) != 1 or not check_password_hash(user_info[0][2], password):
            database.close()
            return redirect("#")            
        
        # Remember which user has logged in
        session["user_id"] = user_info[0][0]
        
        # Close database
        database.close()

        # Redirect user to home page
        return redirect("/")

    # GET
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    # Log user out

    # Forget any user
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    # POST
    if request.method == "POST":
        return "Hello, World!"

    #GET
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Initialize database
    database = sqlite3.connect("users.db")
    db = database.cursor()     

    # POST
    if request.method == "POST":
        # Get username and passwords from user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for valid username               
        names_registered = db.execute("""SELECT username FROM users""")       
        for users in names_registered:
            if not username:
                database.close()
                return redirect("#")
                
            if username == users[0]:
                database.close()
                return redirect("#")                                 

        # Check if entered passwords and they match
        if not password or password != confirmation:
            database.close()
            return redirect("#")
            
        hash = generate_password_hash(password)

        # Register new user into database
        db.execute("""INSERT INTO users (username, hash) VALUES(?, ?)""", (username, hash))

        # Update and close database
        database.commit()
        database.close()
        return render_template("index.html")

    # GET
    return render_template("register.html")

@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
    # Reset all user information

    # POST
    if request.method == "POST":
         
        # Initialize database
        database = sqlite3.connect("users.db")
        db = database.cursor()

        # Reset user info on database
        db.execute("""UPDATE users SET income=?, spendings=? WHERE id=?""", (0, 0, session["user_id"]))

        # Update and close database
        database.commit()
        database.close()

        return redirect("/")

    # GET
    return render_template("reset.html")