from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None
def connect_database(app):
    global db
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1/SART'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db = SQLAlchemy(app)
    return db

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