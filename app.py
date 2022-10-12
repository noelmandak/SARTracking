from flask import Flask, render_template,request
from database import db

app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get('name')

    return render_template("index.html")

@app.route('/register')
def register():
    first_name  = request.args.get('firstname')
    last_name  = request.args.get('lastname')

    full_name = first_name+last_name
    return render_template("welcome.html",full_name=full_name)

@app.route('/login')
def login():
    return render_template("login.html")

