from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "sart"

user = {"sales_admin":"123",
        "finance_admin": "321",
        "manager": "000"}

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1/SART'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class SaleInvoice(db.Model):
    id_transaksi = db.Column('id_transaksi',db.Integer,primary_key=True)
    date = db.Column('tgl_transaksi',db.Date)
    total = db.Column('total',db.Integer)
    id_customer = db.Column('id_customer', db.Integer)
    id_pelunasan = db.Column('id_pelunasan',db.Integer)
    def __init__(self, date, total, id_customer):
        self.date = date
        self.total = total
        self.id_customer = id_customer

class Pelunasan(db.Model):
    id_pelunasan = db.Column('id_pelunasan',db.Integer, primary_key=True)
    date = db.Column('tgl_pelunasan',db.Date)
    total = db.Column('tot_pembayaran',db.Integer)

    def __init__(self, date, total):
        self.date = date
        self.total = total


class Customer(db.Model):
    id_customer = db.Column('id_customer',db.Integer, primary_key=True)
    nama = db.Column('nama',db.String(100))
    alamat = db.Column('alamat',db.String(200))
    telp = db.Column('no_telpon',db.String(20))
    foto = db.Column('foto',db.Text)
    def __init__(self, nama, alamat, telp, foto):
        self.nama = nama
        self.alamat = alamat
        self.telp = telp
        self.foto = foto


@app.route('/')
def hello():
    name = request.args.get('name')
    return render_template("index.html")
    
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

@app.route('/register',methods=['POST'])
def register():
    username  = request.args.get('username')
    password  = request.args.get('password')
    print(username)
    return render_template("welcome.html",full_name=username)

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
    app.run(debug=True)