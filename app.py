import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask import Session
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
            return 
            # Não preencheu nome de usuario!! -------------------------------------------------------
        
        # Check if password was submitted
        if not password:
            return
            # Não preencheu a senha!! ----------------------------------------------------------------

        # Get user info from database
        user_info = db.execute("""SELECT * FROM users WHERE username = ?""", name)

        # Check for valid username and password
        if len(user_info) != 1 or not check_password_hash(user_info[0]["hash"], password):
            return 
            # Nome de usuario ou senha invalidos!! ----------------------------------------------------
        
        # Remember which user has logged in
        session["user_id"] = user_info[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # GET
    return render_template("login.html")


@app.route('/', methods=["GET", "POST"])
def hello():
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
        names_registered = db.execute("SELECT username FROM users")       
        for users in names_registered:
            if not username:
                return redirect("#")
                # Não foi inserido um username ERRO!! --------------------------------------------------------------------
            if username == users[0]:
                return redirect("#")
                # Nome de usuario ja cadastrado!! ------------------------------------------------------------------------                  

        # Check if entered passwords and they match
        if not password or password != confirmation:
            return redirect("#")
            # Não preencheu a senha ou senhas diferentes!! ---------------------------------------------------------------
        hash = generate_password_hash(password)

        # Register new user into database
        db.execute("""INSERT INTO users (username, hash) VALUES(?, ?)""", (username, hash))

        # Update and close database
        database.commit()
        database.close()
        return render_template("index.html")


    # GET
    return render_template("register.html")