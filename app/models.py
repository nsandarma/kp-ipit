from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    nama = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.Integer,nullable=False)
    
class Alumni(db.Model):
    __tablename__ = 'alumni'
    id_alumni = db.Column(db.Integer,primary_key=True)
    nama = db.Column(db.String,nullable=False)
    nim = db.Column(db.String,nullable=False,unique=True)
    email = db.Column(db.String,nullable=False)
    jenis_kelamin = db.Column(db.String,nullable=False)
    tahun = db.Column(db.String,nullable=False)
    status = db.Column(db.String,nullable=False,default=0)
    data_created = db.Column(db.DateTime,default=datetime.now())
    foto = db.Column(db.String,nullable=False)

class pekerjaan(db.Model):
    __tablename__ = 'pekerjaan'
    id = db.Column(db.Integer,primary_key=True)
    perusahaan = db.Column(db.String,nullable=False)
    lokasi = db.Column(db.String,nullable=False)
    job_title = db.Column(db.String,nullable=False)
    deskripsi = db.Column(db.String,nullable=False)
    user_created = db.Column(db.String)
    data_created = db.Column(db.DateTime,default=datetime.now())

class Agenda(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    konten = db.Column(db.String,nullable=False)
    jadwal = db.Column(db.String)
    banner = db.Column(db.String)
    commit = db.Column(db.String)
    data_created = db.Column(db.DateTime,default=datetime.now())
