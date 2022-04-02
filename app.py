import sqlite3
from flask import Flask, render_template, request
from helpers import login_required, usd
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize database
database = sqlite3.connect("finance.db")
db = database.cursor()


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello():
    # POST
    if request.method == "POST":
        return "Hello, World!"


    #GET
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
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
                return 
                # Não foi inserido um username ERRO!! --------------------------------------------------------------------
            if username == users["username"]:
                return
                # Nome de usuario ja cadastrado!! ------------------------------------------------------------------------                  

        # Check if entered passwords and they match
        if not password or password != confirmation:
            return
            # Não preencheu a senha ou senhas diferentes!! ---------------------------------------------------------------
        hash = generate_password_hash(password)

        # Register new user into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return render_template("index.html", username=username, password=password)


    # GET
    return render_template("register.html")