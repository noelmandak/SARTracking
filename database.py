from asyncio.windows_events import NULL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pandas import isnull
from requests import session
from sqlalchemy.dialects import postgresql
from sqlalchemy import func
import datetime


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
    status = db.Column('status',db.String(100))

    def __init__(self, date, total, status):
        self.date = date
        self.total = total
        self.status = status


class Customer(db.Model):
    id_customer = db.Column('id_customer',db.Integer, primary_key=True)
    nama = db.Column('nama',db.String(100))
    alamat = db.Column('alamat',db.String(200))
    telp = db.Column('no_telpon',db.String(20))
    foto = db.Column('foto',db.Text)
    status = db.Column('status',db.String(100))
    def __init__(self, nama, alamat, telp, foto, status):
        self.nama = nama
        self.alamat = alamat
        self.telp = telp
        self.foto = foto
        self.status = status

class Admin(db.Model):
    username = db.Column('username',db.String(100),primary_key=True)
    password = db.Column('password',db.String(100))
    jabatan = db.Column('jabatan',db.String(100))
    def __init__(self, username, password, jabatan):
        self.username = username
        self.password = password
        self.jabatan = jabatan

def get_login_info(curr_username):
    with app.app_context():
        user = Admin.query.filter_by(username=curr_username).first()
        result = [user.username,user.password,user.jabatan]
        print(result)
        return result
# get_login_info('Patrick')

def initiate_table():
    with app.app_context():
        db.drop_all()
        db.create_all()
        adm1 = Admin('Patrick','123','manager')
        adm2 = Admin('Noel','123','sales_admin')
        adm3 = Admin('Tiff','123','finance_admin')
        db.session.add_all([adm1,adm2,adm3])
        db.session.commit()

def invoice_lookup():
    with app.app_context():
        # invoices = SaleInvoice.query.all()
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto).join(Customer, SaleInvoice.id_customer == Customer.id_customer).order_by(SaleInvoice.date).all() # decending (baru ke lama)
        result = [r for r in invoices]
        print(result)
        return result
# invoice_lookup()

def invoice_by_id(id):
    with app.app_context():
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter(Customer.id_customer==id).order_by(SaleInvoice.date)
        # db.session.query(invoices.exists())
        result = [r for r in invoices]
        print(result)
        return result
# invoice_by_name('Jabez')

def unpaid_invoice_by_id(id):
    with app.app_context():
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter(Customer.id_customer.like(id),SaleInvoice.id_pelunasan.is_(None)).order_by(SaleInvoice.date)
        result = [r for r in invoices]
        print(result)
        return result
# unpaid_invoice_by_id(2)

def add_invoice(id_customer,total,date):
    with app.app_context():
        new_inv = SaleInvoice(date, total, id_customer)
        db.session.add(new_inv)
        db.session.commit()
        print('success')
        return 'Success'

# x = datetime.datetime(2020, 5, 17)
# add_invoice(2,400000,x)

def get_all_customer_name():
    with app.app_context():
        customers = Customer.query.all()
        result = [(r.id_customer,r.nama) for r in customers]
        print(result)
        return result
# get_all_customer_name()

def create_customer(nama, alamat, telp, foto):
    with app.app_context():
        new_cust = Customer(nama, alamat, telp, foto, 'active')
        db.session.add(new_cust)
        db.session.commit()
        print('success')
        return 'Success'
# create_customer('Bryan','jl. siapaajygpenting 22','0866666666','Bryan.jpg')

def delete_customer(id):
    with app.app_context():
        Customer.query.filter(Customer.id_customer == id).delete()
        print('success')
        return 'Success'
# delete_customer(3)

def edit_customer(id,new_val,to_edit):
    with app.app_context():
        q = Customer.query.filter_by(id_customer=id).first()
        if to_edit == 'nama':
            q.nama = new_val
        elif to_edit == 'alamat':
            q.alamat = new_val
        elif to_edit == 'no_telpon':
            q.no_telpon = new_val
        elif to_edit == 'foto':
            q.foto = new_val
        db.session.commit()
        print('edited')
        return "Edited"

# edit_customer(2,'j suka m','alamat')

# Edit data customer status
def change_customer_status(id):
    with app.app_context():
        q = Customer.query.filter_by(id_customer=id).first()
        if q.status == 'active':
            q.status = 'inactive'
        else:
            q.status = 'active'
        db.session.commit()
        print('edited')
        return "Edited"
# change_customer_status(1)

# get detail customer data by id, return nama, alamat, no tlp, foto, status, terbayar, blm terbayar, semua invoice dgn nama dia
def get_detail_customer(id):
    with app.app_context():
        result = []
        q = Customer.query.filter_by(id_customer=id).first()
        result.append(q.nama)
        result.append(q.alamat)
        result.append(q.telp)
        result.append(q.foto)
        paid = db.session.query(func.sum(SaleInvoice.total).label('total')).filter(SaleInvoice.id_customer.like(id),SaleInvoice.id_pelunasan == None)
        notpaid = db.session.query(func.sum(SaleInvoice.total).label('total')).filter(SaleInvoice.id_customer.like(id),SaleInvoice.id_pelunasan != None)
        paid = [r for r, in paid][0]
        notpaid = [r for r, in notpaid][0]
        result.append(paid)
        result.append(notpaid)
        invoice = invoice_by_id(id)
        result.append(invoice)
        return result
# get_detail_customer(1)

# Total piutang perusahaan

# total piutang 1 orang

# total sudah dibayar 1 orang

# edit terbayar

# bikin pelunasan (list id trans, tanggal, total)

# get all return id_cus, nama, tot_utang, status, foto

# get foto by id





