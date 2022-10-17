from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sart"

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

class Admin(db.Model):
    username = db.Column('username',db.String(100),primary_key=True)
    password = db.Column('password',db.String(100))
    jabatan = db.Column('jabatan',db.String(100))
    def __init__(self, username, password, jabatan):
        self.username = username
        self.password = password
        self.jabatan = jabatan

def get_user(curr_username):
    user = Admin.query.filter_by(username=curr_username).first()
    return user

def initiate_table():
    with app.app_context():
        db.drop_all()
        db.create_all()
        adm1 = Admin('Patrick','123','manager')
        adm2 = Admin('Noel','123','sales_admin')
        adm3 = Admin('Tiff','123','finance_admin')
        db.session.add_all([adm1,adm2,adm3])
        db.session.commit()
# initiate_table()