from unicodedata import name
from flask import Flask, render_template,request,session,redirect,url_for,flash
from database import *
import socket
import json

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


@app.route('/login',methods=['POST','GET'])    # type: ignore
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
    return render_template("sale.html",name=name, all_invoice=all_invoice,role=role)


@app.route('/new_invoice',methods=['POST',"GET"])
def new_invoice():
    if not role_verify("sales_admin"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
    
    if request.method == 'POST':
        customer_name  = request.form['customer-name']
        total  = request.form['total']
        date  = request.form['date']
        # print(customer_name,total,date)
        message = add_invoice(customer_name,total,date)

        flash(f"New Invoice Added",category=message)
        return redirect(url_for("sales_admin"))

    all_customer = get_all_customer_name()
    return render_template("new_invoice.html", all_customer=all_customer)





##### Finance Admin #####
@app.route('/finance_admin')
def finance_admin():
    if not role_verify("finance_admin"):
        flash("Akses ditolak")
        return redirect(url_for("home"))

    
    name = session["name"]
    all_invoice = invoice_lookup()

    return render_template("finance.html",name=name,all_invoice=all_invoice)

@app.route('/mark_invoice', methods=["POST"])
def mark_invoice():
    if not role_verify("finance_admin"):
        flash("Akses ditolak")
        return redirect(url_for("home"))

    if request.method == 'POST':
        id_transactions = request.form['selected']
        id_transactions=json.loads(id_transactions)['transactions']
        date = request.form['date']
        message = make_pelunasan(id_transactions,date)
        flash(f"{len(id_transactions)} Transaction has paid",category=message)
    
    return redirect(url_for("finance_admin"))



##### Manager #####
@app.route('/manager')
def manager():
    if not role_verify("manager"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
        
    name = session["name"]
    total_piutang = show_piutang_perusahaan()
    total_piutang = f'{total_piutang:,}'
    return render_template("manager.html",name=name,total_piutang=total_piutang)


@app.route('/new_customer', methods=['POST', 'GET'])
def new_customer():
    if not role_verify("manager"):
        flash("Akses ditolak")
        return redirect(url_for("home"))

    if request.method == 'POST':
        name = request.form['username']
        phone_number = request.form['phone-number']
        address = request.form['address']
        profile_pict =  'images/tiff.png'
        # profile_pict =  request.form['profile_pict']'
        message = create_customer(name, address, phone_number, profile_pict)
        flash("New customer successfully added.", category=message)
        return redirect(url_for("data_customer"))

    return render_template("new_customer.html")


@app.route('/data_customer')
def data_customer():
    if not role_verify("manager"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
    
    customers = get_all_customer_name()
    data_customers = []
    for id, name in customers:
        total = total_notpaid_by_id(id)
        img = get_foto_by_id(id)
        status = get_status_customer_by_id(id)
        data_customers.append([id,name,f'{total:,}',url_for('static',filename=img),status])

@app.route("/detail_customer")
def detail_customer():
    # id = request.form['id']
    id=1
    nama,alamat,no_tlp,foto,status,paid,unpaid,invoices = get_detail_customer(id)
    if unpaid != None and paid !=None:
        total = unpaid+paid
    elif unpaid != None:
        total = unpaid
    elif paid != None:
        total = paid
    else:
        total = 0
    return render_template("detail_customer.html",nama=nama,alamat=alamat,no_tlp=no_tlp,foto=url_for('static',filename=foto),status=status,paid=paid,unpaid=unpaid,invoices=invoices,total=total)

@app.route("/data_transaction")
def data_transaction():
    if not role_verify("manager"):
        flash("Akses ditolak")
        return redirect(url_for("home"))
        
    print(invoice_lookup_with_status())
    all_invoice = invoice_lookup_with_status()
    return render_template("data_transaction.html",all_invoice=all_invoice)






@app.route("/popup")
def popup():
    return render_template("detail_customer.html")



# import os

# def coba():
#     if request.method == 'POST':
#         if 'file1' not in request.files:
#             return 'there is no file1 in form!'
#         file1 = request.files['file1']
#         path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
#         file1.save(path)
#         return path
#     return '''
#     <h1>Upload new File</h1>
#     <form method="post" enctype="multipart/form-data">
#     <input type="file" name="file1">
#     <input type="submit">
#     </form>
#     '''
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '\static\images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/coba', methods = ['POST','GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
if __name__ == '__main__':
    initiate_table()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.run(host=ip_address, port=5000, debug=True, threaded=False)