import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, usd
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

    # POST
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        # Check if username and password were submitted
        if not name or not password:
            return redirect("#")  

        # Initialize database
        database = sqlite3.connect("users.db")
        db = database.cursor()                 

        # Get user info from database
        db.execute("SELECT * FROM users WHERE username=?", (name,))     
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
    
    date = datetime.now().date()
    month = date.month
    year = date.year

    # List of expenses 
    expense_items = {"Transportation": 0, "Housing": 0, "Medical/Health": 0, "Groceries": 0, "Insurance": 0, "Shopping": 0, "Hobbies/Entertainment": 0, "Others": 0}

    # Initialize database
    database = sqlite3.connect("users.db")
    db = database.cursor()

    # POST 
    if request.method == "POST":

        # Get month and year
        month = request.form.get("month")
        year = request.form.get("year")

        # Check if user selected month and year
        if not month or not year:
            database.close()
            return redirect("#")        

        # Get usename
        db.execute("SELECT username FROM users WHERE id=?", (session["user_id"],))
        name = db.fetchall()

        # Get data from selected month and year
        db.execute("SELECT * FROM expenses WHERE user_id=? AND month=? AND year=?", (session["user_id"], month, year))
        expenses = db.fetchall()
        db.execute("SELECT * FROM user_history WHERE user_id=? AND date=?", (session["user_id"], f"{month}/{year}"))
        history = db.fetchall()

        # Check if user has expenses on the selected date
        if len(expenses) != 1:
            database.close()
            return redirect("#")
            
        # Divide expenses into types            
        for items in history:
            if items[2] == "spending":             
                expense_items[items[3]] += items[5]

        # Get % values of each expense_items compared to the total spent and pass it as a list to index.html
        user_income = expenses[0][1]
        user_spending = expenses[0][2]
        expenses_fraction = []
        if user_spending > 0:            
            for i in expense_items:
                fraction = expense_items[i] / user_spending
                expenses_fraction.append(fraction)              
        else:
            expenses_fraction = [0, 0, 0, 0, 0, 0, 0, 0]

        # Close database and return POST
        database.close()
        return render_template("index.html", expenses=expenses_fraction, year=int(year), month=month, income=usd(user_income), spending=usd(user_spending))

    # GET  
    database.close()
    return render_template("index.html",expenses=None, year=year, month=month)

@app.route("/register", methods=["GET", "POST"])
def register():    

    # POST
    if request.method == "POST":
        # Get username and passwords from user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if entered passwords and they match
        if not password or password != confirmation:            
            return redirect("#")

        # Initialize database
        database = sqlite3.connect("users.db")
        db = database.cursor()  
            
        # Check for valid username               
        names_registered = db.execute("SELECT username FROM users")       
        for users in names_registered:
            if not username:
                database.close()
                return redirect("#")
                
            if username == users[0]:
                database.close()
                return redirect("#")                        
        
        hash = generate_password_hash(password)

        # Register new user into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))

        # Update and close database
        database.commit()
        database.close()
        return redirect("/login")

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
        date = datetime.now().date()
        db.execute("DELETE FROM expenses WHERE user_id=?", (session["user_id"],))
        db.execute("DELETE FROM user_history WHERE user_id=?", (session["user_id"],))

        # Update and close database
        database.commit()
        database.close()

        return redirect("/")

    # GET
    return render_template("reset.html")

@app.route("/income", methods=["GET", "POST"])
@login_required
def add_income():
    # Add user income

    # POST
    if request.method == "POST":
        income_type = request.form.get("income")
        amount = request.form.get("amount")  
        month = request.form.get("month")     
        year = request.form.get("year")

        # Check if user filled all fields
        if not income_type or not month or not year:            
            return redirect("#")
        
        # Check for valid amount
        try:
            if not amount or float(amount) <= 0:                
                return redirect("#")
        except ValueError:            
            return redirect("#")
            # Nao informou amount valida --------------------------------------------------

         # Initialize database
        database = sqlite3.connect("users.db")
        db = database.cursor()        

        # Check if month and year already exist in expenses then update income
        db.execute("SELECT * FROM expenses WHERE month=? AND year=?", (month, year))
        exist = db.fetchall()
        if len(exist) != 1:
            db.execute("INSERT INTO expenses (user_id, income, month, year) VALUES(?, ?, ?, ?)", (session["user_id"], float(amount), month, year))
        else:
            # Get current income from user
            db.execute("SELECT income FROM expenses WHERE user_id=? AND month=? AND year=?", (session["user_id"], month, year))
            current_income = db.fetchall()
            new_income = current_income[0][0] + float(amount)            
            db.execute("UPDATE expenses SET income=? WHERE month=? AND year=? AND user_id=?", (new_income, month, year, session["user_id"]))        

        db.execute("INSERT INTO user_history (user_id, spending, type, description, amount, date) VALUES(?, ?, ?, ?, ?, ?)", (session["user_id"], "income", income_type, "", float(amount), f"{month}/{year}"))

        # Update and close database
        database.commit()
        database.close()

        return redirect("/")

    # GET
    date = datetime.now().date()
    return render_template("income.html", year=date.year)

@app.route("/spending", methods=["GET", "POST"])
@login_required
def spending():
    # Add new spending

    # List of expenses
    expenses = ["Transportation", "Housing", "Medical/Health", "Groceries", "Insurance", "Shopping", "Hobbies/Entertainment", "Others"]

    # POST
    if request.method == "POST":
        expense = request.form.get("expense")
        item = request.form.get("item")
        price = request.form.get("price")
        amount = request.form.get("amount")
        month = request.form.get("month")
        year = request.form.get("year")

        # Check is user filled all fields
        if not expense or not item or not price or not amount or not month or not year:
            return redirect("#")

        # Check if selected valid expense
        if expense not in expenses:
            return redirect("#")

        # Check if valid price and amount
        try:
            if int(amount) <= 0 or float(price) <= 0:
                return redirect("#")
        except ValueError:
            return redirect("#")

        cost = int(amount) * float(price)

        # Initialize database
        database = sqlite3.connect("users.db")
        db = database.cursor()

        # Check if month and year already exist in expenses then update spendings
        db.execute("SELECT * FROM expenses WHERE month=? AND year=?", (month, year))
        exist = db.fetchall()
        if len(exist) != 1:
            db.execute("INSERT INTO expenses (user_id, spendings, month, year) VALUES(?, ?, ?, ?)", (session["user_id"], cost, month, year))
        else:

            # Get current spendings from user 
            db.execute("SELECT spendings FROM expenses WHERE user_id=? AND month=? AND year=?", (session["user_id"], month, year))
            current_spendings = db.fetchall()

            # Calculate new spending value            
            new_spendings = float(current_spendings[0][0]) + cost

            db.execute("UPDATE expenses SET spendings=? WHERE month=? AND year=? AND user_id=?", (new_spendings, month, year, session["user_id"]))   
        db.execute("INSERT INTO user_history (user_id, spending, type, description, amount, date) VALUES(?, ?, ?, ?, ?, ?)", (session["user_id"], "spending", expense, item, cost, f"{month}/{year}"))
        

        # Update and close database
        database.commit()
        database.close()

        return redirect("/")

    # GET
    date = datetime.now().date()
    return render_template("spending.html", expenses=expenses, year=date.year)

@app.route("/history")
@login_required
def history():
    # Show users history

    # Initialize database
    database = sqlite3.connect("users.db")
    db = database.cursor()

    # Get users history
    db.execute("SELECT * FROM user_history WHERE user_id=?", (session["user_id"],))
    history = db.fetchall()
    amount = []

    for items in history:
        amount.append(usd(items[5]))

    # Close database
    database.close()
    return render_template("history.html", history=history, amount=amount)