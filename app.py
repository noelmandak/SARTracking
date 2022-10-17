from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from database import *



app = Flask(__name__)
app.secret_key = "sart"

db = connect_database(app)

@app.route('/')
def home():
    if "username" in session:
        if session["username"] == "sales_admin":
            return redirect(url_for("sales_admin"))
        elif session["username"] == "finance_admin":
            return redirect(url_for("finance_admin"))
        elif session["username"] == "manager":
            return redirect(url_for("manager"))
    else:
        return redirect(url_for("login"))
    
@app.route('/sales_admin')
def sales_admin():
    if "username" in session:
        if session["username"] == "sales_admin":
            return render_template("sale.html")
        else: 
            flash("Akses ditolak")
            return redirect(url_for("login"))
    flash("Login terlebih dahulu")
    return redirect(url_for("login"))

@app.route('/finance_admin')
def finance_admin():
    if "username" in session:
        if session["username"] == "finance_admin":
            return render_template("finance.html")
        else: 
            flash("Akses ditolak")
            return redirect(url_for("login"))
    flash("Login terlebih dahulu")
    return redirect(url_for("login"))

@app.route('/manager')
def manager():
    if "username" in session:
        if session["username"] == "manager":
            return render_template("manager.html")
        else: 
            flash("Akses ditolak")
            return redirect(url_for("login"))
    flash("Login terlebih dahulu")
    return redirect(url_for("login"))

# @app.route('/register',methods=['POST'])
# def register():
#     username  = request.args.get('username')
#     password  = request.args.get('password')
#     print(username)
#     return render_template("welcome.html",full_name=username)

@app.route('/login',methods=['POST',"GET"])
def login():
    if "username" in session:
        if session["username"] == "sales_admin":
            return redirect(url_for("sales_admin"))
        elif session["username"] == "finance_admin":
            return redirect(url_for("finance_admin"))
        elif session["username"] == "manager":
            return redirect(url_for("manager"))

    if request.method == 'POST':
        username  = request.form['username']
        password  = request.form['password']
        if username in user:
            if password == user[username]:
                session['username'] = username
                if username == "sales_admin":
                    return redirect(url_for("sales_admin"))
                elif username == "finance_admin":
                    return redirect(url_for("finance_admin"))
                elif username == "manager":
                    return redirect(url_for("manager"))
            else:
                flash("Gagal, username atau passord tidak cocok")
                return redirect(url_for("login"))
            
        else:
            flash("Gagal, user tidak ditemukan")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='10.252.243.187', port=5000, debug=True, threaded=False)