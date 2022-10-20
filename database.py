from unittest import result
from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sart"

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1/SART'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class SaleInvoice(db.Model):  # type: ignore
    id_transaksi = db.Column('id_transaksi',db.Integer,primary_key=True)
    date = db.Column('tgl_transaksi',db.Date)
    total = db.Column('total',db.Integer)
    id_customer = db.Column('id_customer', db.Integer)
    id_pelunasan = db.Column('id_pelunasan',db.Integer)
    def __init__(self, date, total, id_customer):
        self.date = date
        self.total = total
        self.id_customer = id_customer

class Pelunasan(db.Model):  # type: ignore
    id_pelunasan = db.Column('id_pelunasan',db.Integer, primary_key=True)
    date = db.Column('tgl_pelunasan',db.Date)
    total = db.Column('tot_pembayaran',db.Integer)
    status = db.Column('status',db.String(100))

    def __init__(self, date, total, status):
        self.date = date
        self.total = total
        self.status = status


class Customer(db.Model):  # type: ignore
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

class Admin(db.Model):  # type: ignore
    username = db.Column('username',db.String(100),primary_key=True)
    name = db.Column('name',db.String(100))
    password = db.Column('password',db.String(100))
    jabatan = db.Column('jabatan',db.String(100))
    def __init__(self, username, name, password, jabatan):
        self.username = username
        self.name = name
        self.password = password
        self.jabatan = jabatan

def get_login_info(curr_username):
    with app.app_context():
        user = Admin.query.filter_by(username=curr_username).first()
        if user != None: return [user.username,user.name,user.password,user.jabatan]
        return None
# get_login_info('Patrick')

def initiate_table():
    with app.app_context():
        db.drop_all()
        db.create_all()
        adm1 = Admin('Patrick','James Patrick Oentoro','123','manager')
        adm2 = Admin('Noel','Noel Christevent Mandak','123','sales_admin')
        adm3 = Admin('Tiff', 'Tiffany Sondakh','123','finance_admin')
        db.session.add_all([adm1,adm2,adm3])
        db.session.commit()
        add_dummy_data()

def add_dummy_data():    
    with app.app_context():
        nama = ["Elsa Nove Teresia","Audrey Josephine","Evan Christopher","Victor Chendra","Grace Melissa Khoe Ping Ing"]
        alamat_rmci = ["Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1720, lt. 8 ",
                       "Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1820, lt. 8 ",
                       "Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1926, lt. 8 ",
                       "Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1926, lt. 8 ",
                       "Jl. Industri Blok B14, RW 10, Pademangan Timur, Kemayoran, Jakarta 10610, CIT 1705, lt. 8 "]
        no_telp = ["0812-2333-0000","0812-2333-0001","0812-2333-0002","0812-2333-0003","0812-2333-0004"]
        foto = ["images/elsa.png","images/udey.png","images/evan.png","images/victor.png","images/ping.png"]
        status = ["active","non-active","non-active","active","active"]
        for i in range(5):
            customer = Customer(nama[i],alamat_rmci[i],no_telp[i],foto[i],status[i])
            db.session.add(customer)
        db.session.commit()

        invoice = [["2022-10-20", "123000", "2"],["2022-10-20", "100000", "1"],["2022-10-20", "21000", "5"],["2022-10-20", "60000", "4"],["2022-10-20", "200000", "3"]]        
        for date,total, id_customer in invoice: add_invoice(id_customer,total,date)

def invoice_lookup():
    with app.app_context():
        # invoices = SaleInvoice.query.all()
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter(SaleInvoice.id_pelunasan==None).order_by(SaleInvoice.id_transaksi.desc()).all() # decending (baru ke lama)
        print("hoho",invoices)
        result = [[id,name,f'{total:,}',date.strftime("%d/%m/%Y"),url_for('static',filename=img)] for id,name,total,date,img in invoices]
        return result

def invoice_lookup_with_status():
    with app.app_context():
        # invoices = SaleInvoice.query.all()
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto,SaleInvoice.id_pelunasan).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter((SaleInvoice.id_pelunasan>0)|(SaleInvoice.id_pelunasan==None)).order_by(SaleInvoice.id_transaksi.desc()).all() # decending (baru ke lama)
        result = []
        for id,name,total,date,img,pelunasan in invoices:
            if pelunasan==None : is_paid = "Unpaid"
            else: is_paid = "Paid"
            result.append([id,name,f'{total:,}',date.strftime("%d/%m/%Y"),url_for('static',filename=img),pelunasan,is_paid])
        return result
# invoice_lookup()

def invoice_by_id(id):
    with app.app_context():
        invoices = db.session.query(SaleInvoice.id_transaksi, Customer.nama, SaleInvoice.total, SaleInvoice.date, Customer.foto, SaleInvoice.id_pelunasan).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter(Customer.id_customer==id).order_by(SaleInvoice.date)
        # db.session.query(invoices.exists())
        result = [r for r in invoices]
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
        return 'success'

# x = datetime.datetime(2020, 5, 17)
# add_invoice(2,400000,x)

def get_all_customer_name():
    with app.app_context():
        customers = Customer.query.all()
        result = [(r.id_customer,r.nama) for r in customers]
        print(result)
        return result
# get_all_customer_name()

def get_active_customer_name():
    with app.app_context():
        customers = Customer.query.filter(Customer.status=="active").all()
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
            q.status = 'non-active'
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
        # invoices = db.session.query( Customer.nama, Customer.alamat, Customer.telp, Customer.foto, Customer.status).join(Customer, SaleInvoice.id_customer == Customer.id_customer).filter(Customer.id_customer==id).order_by(SaleInvoice.date)
        q = Customer.query.filter_by(id_customer=id).first()
        result.append(q.nama)
        result.append(q.alamat)
        result.append(q.telp)
        result.append(q.foto)
        result.append(q.status)
        notpaid = total_notpaid_by_id(id)
        paid = total_paid_by_id(id)
        result.append(paid)
        result.append(notpaid)
        invoices = db.session.query(SaleInvoice.date, SaleInvoice.total, SaleInvoice.id_pelunasan, Pelunasan.date).join(Pelunasan, SaleInvoice.id_pelunasan == Pelunasan.id_pelunasan, isouter=True).filter(SaleInvoice.id_customer==id).order_by(SaleInvoice.date)
        transactions = []

        for tgl_piutang, total, id_pelunasan, tgl_lunas in invoices:
            tgl_piutang=tgl_piutang.strftime("%d/%m/%Y")
            total=f'{total:,}'
            if tgl_lunas==None : ket = "Unpaid"
            else: ket = f'Paid at {tgl_lunas.strftime("%d/%m/%Y")}'
            transactions.append([tgl_piutang,ket,total])
        result.append(transactions)
        return result


    
# Total piutang perusahaan
def show_piutang_perusahaan():
    with app.app_context():
        result = db.session.query(func.sum(SaleInvoice.total).label('total')).filter(SaleInvoice.id_pelunasan == None)
        result = [r for r, in result][0]
        print(result)
        return result
# show_piutang_perusahaan()

# total piutang 1 orang
def total_paid_by_id(id):
    with app.app_context():
        paid = db.session.query(func.sum(SaleInvoice.total).label('total')).filter(SaleInvoice.id_customer.like(id),SaleInvoice.id_pelunasan != None)
        paid = [r for r, in paid][0]
        return paid

# total sudah dibayar 1 orang
def total_notpaid_by_id(id):
    with app.app_context():
        notpaid = db.session.query(func.sum(SaleInvoice.total).label('total')).filter(SaleInvoice.id_customer.like(id),SaleInvoice.id_pelunasan == None)
        notpaid = [r for r, in notpaid][0]
        return notpaid

# edit terbayar
def paid(id_transaksi,id_pelunasan):
    with app.app_context():
        q = SaleInvoice.query.filter(SaleInvoice.id_transaksi==id_transaksi).first()
        q.id_pelunasan = id_pelunasan
        db.session.commit()
        print('edited')
        return "Edited"

# bikin pelunasan (list id trans, tanggal, total)
def make_pelunasan(list_invoice_id,tanggal):
    with app.app_context():
        total = 0
        for invoice in list_invoice_id:
            q = SaleInvoice.query.filter(SaleInvoice.id_transaksi==invoice).first()
            total+=q.total
        pelunasan = Pelunasan(tanggal, total, None)
        db.session.add(pelunasan)
        db.session.commit()
        for invoice in list_invoice_id:
            paid(invoice,pelunasan.id_pelunasan)
        return 'success'
# make_pelunasan([1,2],datetime.datetime(2023, 5, 17))

# get all return id_cus, nama, tot_utang, status, foto
def get_customer_unpaid_data(id):
    with app.app_context():
        result = []
        q = Customer.query.filter(Customer.id_customer==id).first()
        result.append(q.id_customer)
        result.append(q.nama)
        tot_hutang = total_notpaid_by_id(id)
        result.append(tot_hutang)
        result.append(q.status)
        result.append(q.foto)
        print(result)
        return result
# get_customer_unpaid_data(1)

# get foto by id
def get_foto_by_id(id):
    with app.app_context():
        foto = Customer.query.filter(Customer.id_customer == id).first().foto
        print(foto)
        return foto
# get_foto_by_id(1)

def get_status_customer_by_id(id):
    with app.app_context():
        status = Customer.query.filter(Customer.id_customer == id).first().status
        return status

def void(id_pelunasan):
    with app.app_context():
        q = Pelunasan.query.filter(Pelunasan.id_pelunasan == id_pelunasan).first()
        q.status = 'void'
        invoices = SaleInvoice.query.filter(SaleInvoice.id_pelunasan == id_pelunasan).all()
        for invoice in invoices:
            invoice.id_pelunasan = None
            # invoice.id_pelunasan = -1
        db.session.commit()
        return 'success'
# void(2)

def id_pelunasan_to_all_invoice(id_pelunasan):
    print("idpelunsan",id_pelunasan)
    with app.app_context():
        q = db.session.query(Customer.nama,Customer.foto,SaleInvoice.date,SaleInvoice.total,Pelunasan.date).join(Customer,SaleInvoice.id_customer==Customer.id_customer).filter(SaleInvoice.id_pelunasan==id_pelunasan).all()
        result = [[nama ,url_for('static',filename=foto),date_trans.strftime("%d/%m/%Y"),f'{total:,}',date_paid.strftime("%d/%m/%Y")] for nama,foto,date_trans,total,date_paid in q]
        print(result)
        return result
# id_pelunasan_to_all_invoice(1)

