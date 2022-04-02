from flask import Flask, render_template, request

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


    # GET
    return render_template("register.html")