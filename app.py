from colorama import init
from flask import Flask, render_template,request,session,redirect,url_for,flash
from database import *
import socket

def role_verify(jabatan):
    if "jabatan" in session:
        if session["jabatan"] == jabatan: return True
    return False


@app.route('/')
def home():
    if "jabatan" in session:
        if session["jabatan"] == "sales_admin":
            return redirect(url_for("sales_admin"))
        elif session["jabatan"] == "finance_admin":
            return redirect(url_for("finance_admin"))
        elif session["jabatan"] == "manager":
            return redirect(url_for("manager"))
        else:
            flash("Akses ditolak, silahkan login dahulu")
            return redirect(url_for("logout"))
    else:
        return redirect(url_for("login"))


@app.route('/login',methods=['POST',"GET"])
def login():
    if "jabatan" in session:
        if session["jabatan"] == "sales_admin":
            return redirect(url_for("sales_admin"))
        elif session["jabatan"] == "finance_admin":
            return redirect(url_for("finance_admin"))
        elif session["jabatan"] == "manager":
            return redirect(url_for("manager"))

    if request.method == 'POST':
        curr_username  = request.form['username']
        curr_password  = request.form['password']
        curr_user = get_login_info(curr_username) #[username, name, password, jabatan]
        if curr_user is not None:
            if curr_user[2] == curr_password:
                session['jabatan'] = curr_user[3]
                session['name'] = curr_user[1]
                if   session['jabatan'] == "sales_admin"  : return redirect(url_for("sales_admin"))
                elif session['jabatan'] == "finance_admin": return redirect(url_for("finance_admin"))
                elif session['jabatan'] == "manager"      : return redirect(url_for("manager"))
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





##### Sales Admin #####
@app.route('/sales_admin')
def sales_admin():
    if not role_verify("sales_admin"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
    name = session["name"]
    all_invoice = invoice_lookup()
    print(all_invoice)
    # for i in range(len(all_invoice)):
    #     print(f'{all_invoice[i][2]:,}')
    #     all_invoice[i][2] = f'{all_invoice[i][2]:,}'
    return render_template("sale.html",username=name, all_invoice=all_invoice)


@app.route('/new_invoice',methods=['POST',"GET"])
def new_invoice():
    if not role_verify("sales_admin"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
    
    if request.method == 'POST':
        
        customer_name  = request.form['customer-name']
        total  = request.form['total']
        date  = request.form['date']
        print(customer_name,total,date)
        message = add_invoice(customer_name,total,date)

        flash(f"New Invoice Added",category=message)
        return redirect(url_for("sales_admin"))


    all_customer = get_all_customer_name()
    
    
    

    return render_template("new_invoice.html", all_customer=all_customer)





##### Finance Admin #####
@app.route('/finance_admin')
def finance_admin():
    if role_verify("finance_admin"):
        return render_template("finance.html")
    flash("Akses ditolak")
    return redirect(url_for("home"))





##### Manager #####
@app.route('/manager')
def manager():
    if role_verify("manager"):
        return render_template("manager.html")
    flash("Akses ditolak")
    return redirect(url_for("home"))







@app.route("/popup")
def popup():
    return render_template("detail_customer.html")

@app.route("/detail_customer")
def detail_customer():
    return render_template("detail_customer.html")

@app.route("/data_transaction")
def data_transaction():
    return render_template("data_transaction.html")

@app.route('/new_customer')
def new_customer():
    return render_template("new_customer.html")

@app.route('/data_customer')
def data_customer():
    return render_template("data_customer.html")


if __name__ == '__main__':
    # initiate_table()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.run(host=ip_address, port=5000, debug=True, threaded=False)