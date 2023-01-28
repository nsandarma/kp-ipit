from app.models import Alumni,pekerjaan,Agenda
import pandas as pd

def get_excel(page):
    total_pekerjaan = pekerjaan.query.all()
    agenda = Agenda.query.all()
    nama = []
    nim = []
    email = []
    tempat_lahir = []
    tanggal_lahir = []
    jenis_kelamin= []
    agama = []
    alamat = []
    tahun_lulus = []
    ipk = []
    judul_skripsi = []
    pekerjaan_s = []
    tempat_bekerja = []
    status =[]
    foto =  []
    if page == 'total_alumni':
        q = Alumni.query.all()
        for i in q:
            nama.append(i.nama)
            nim.append(i.nim)
            email.append(i.email)
            tempat_lahir.append(i.tempat_lahir)
            tanggal_lahir.append(i.tanggal_lahir)
            jenis_kelamin.append(i.jenis_kelamin)
            agama.append(i.agama)
            alamat.append(i.alamat)
            ipk.append(i.ipk)
            judul_skripsi.append(i.judul_skripsi)
            pekerjaan_s.append(i.pekerjaan)
            tempat_bekerja.append(i.tempat_bekerja)
            tahun_lulus.append(i.tahun_lulus)
            status.append(i.status)
            foto.append(i.foto)
        data = {
            "nama":nama,
            'nim':nim,
            'email':email,
            'tempat_lahir':tempat_lahir,
            'tanggal_lahir':tanggal_lahir,
            'jenis_kelamin':jenis_kelamin,
            'agama':agama,
            'alamat':alamat,
            'tahun_lulus':tahun_lulus,
            'ipk' :ipk,
            'judul_skripsi' :judul_skripsi,
            'pekerjaan':pekerjaan_s,
            'tempat_bekerja':tempat_bekerja,
            'status':status,
            'foto':foto,
        }
        df = pd.DataFrame(data)
        uri = f'app/data/{page}.xlsx'
        df.to_excel(uri)
    elif page == 'alumni_unverified':
        q = Alumni.query.filter_by(status='unverified').all()
        for i in q:
            nama.append(i.nama)
            nim.append(i.nim)
            email.append(i.email)
            tempat_lahir.append(i.tempat_lahir)
            tanggal_lahir.append(i.tanggal_lahir)
            jenis_kelamin.append(i.jenis_kelamin)
            agama.append(i.agama)
            alamat.append(i.alamat)
            ipk.append(i.ipk)
            judul_skripsi.append(i.judul_skripsi)
            pekerjaan_s.append(i.pekerjaan)
            tempat_bekerja.append(i.tempat_bekerja)
            tahun_lulus.append(i.tahun_lulus)
            status.append(i.status)
            foto.append(i.foto)
        data = {
            "nama":nama,
            'nim':nim,
            'email':email,
            'tempat_lahir':tempat_lahir,
            'tanggal_lahir':tanggal_lahir,
            'jenis_kelamin':jenis_kelamin,
            'agama':agama,
            'alamat':alamat,
            'tahun_lulus':tahun_lulus,
            'ipk' :ipk,
            'judul_skripsi' :judul_skripsi,
            'pekerjaan':pekerjaan_s,
            'tempat_bekerja':tempat_bekerja,
            'status':status,
            'foto':foto,
        }
        df = pd.DataFrame(data)
        uri = f'app/data/{page}.xlsx'
        df.to_excel(uri)
    elif page == 'alumni_verified':
        q = Alumni.query.filter_by(status='verified').all()
        for i in q:
            nama.append(i.nama)
            nim.append(i.nim)
            email.append(i.email)
            tempat_lahir.append(i.tempat_lahir)
            tanggal_lahir.append(i.tanggal_lahir)
            jenis_kelamin.append(i.jenis_kelamin)
            agama.append(i.agama)
            alamat.append(i.alamat)
            ipk.append(i.ipk)
            judul_skripsi.append(i.judul_skripsi)
            pekerjaan_s.append(i.pekerjaan)
            tempat_bekerja.append(i.tempat_bekerja)
            tahun_lulus.append(i.tahun_lulus)
            status.append(i.status)
            foto.append(i.foto)
        data = {
            "nama":nama,
            'nim':nim,
            'email':email,
            'tempat_lahir':tempat_lahir,
            'tanggal_lahir':tanggal_lahir,
            'jenis_kelamin':jenis_kelamin,
            'agama':agama,
            'alamat':alamat,
            'tahun_lulus':tahun_lulus,
            'ipk' :ipk,
            'judul_skripsi' :judul_skripsi,
            'pekerjaan':pekerjaan_s,
            'tempat_bekerja':tempat_bekerja,
            'status':status,
            'foto':foto,
        }
        df = pd.DataFrame(data)
        uri = f'app/data/{page}.xlsx'
        df.to_excel(uri)
    elif page == 'pekerjaan':
        perusahaan,lokasi,job_title,deskripsi = [],[],[],[]
        for i in total_pekerjaan:
            perusahaan.append(i.perusahaan)
            lokasi.append(i.lokasi)
            job_title.append(i.job_title)
            deskripsi.append(i.deskripsi)
        data = {
            "perusahaan":perusahaan,
            'lokasi':lokasi,
            'job_title':job_title,
            'deksripsi':deskripsi
        }
        df = pd.DataFrame(data)
        uri = f'app/data/{page}.xlsx'
        df.to_excel(uri)
    elif page == 'agenda':
        title,konten,jadwal,banner = [],[],[],[]
        for i in agenda:
            title.append(i.title)
            konten.append(i.konten)
            jadwal.append(i.jadwal)
            banner.append(i.banner)
        data = {
            'title':title,
            'konten':konten,
            'jadwal':jadwal,
            'banner':banner
        }
        df = pd.DataFrame(data)
        uri = f'app/data/{page}.xlsx'
        df.to_excel(uri)


