from flask import Flask, render_template,request,session,redirect,url_for,flash
from database import *




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
    else:
        return redirect(url_for("login"))
    
@app.route('/sales_admin')
def sales_admin():
    # if "username" in session:
    #     if session["username"] == "sales_admin":
    #         return render_template("sale.html")
    #     else: 
    #         flash("Akses ditolak")
    #         return redirect(url_for("login"))
    # flash("Login terlebih dahulu")
    # return redirect(url_for("login"))
    return render_template("sale.html")

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
        curr_username  = request.form['username']
        curr_password  = request.form['password']
        curr_user = get_user(curr_username)
        if curr_user is not None:
            if str(curr_user.password) == curr_password:
                session['username'] = curr_user.jabatan
                if curr_user.jabatan == "sales_admin":
                    return redirect(url_for("sales_admin"))
                elif curr_user.jabatan == "finance_admin":
                    return redirect(url_for("finance_admin"))
                elif curr_user.jabatan == "manager":
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
    app.run(host='10.237.78.240', port=5000, debug=True, threaded=False)