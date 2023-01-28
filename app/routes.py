from app import app,render_template,redirect,request,session,Alumni,User,db,secure_filename,generate_password_hash,check_password_hash,pekerjaan,Agenda,get_excel,send_file,send_notif
import pandas as pd
import os


@app.route('/')
def home():
    user = session.get('user')
    if user:
        if user == 'admin':
            return redirect('/admin')
        elif user != 'admin':
            return redirect('/user')
    else:
        alumni = Alumni.query.all()
        return render_template('index.html',alumni=alumni)
@app.route('/cek_status',methods=['GET','POST'])
def cek_status():
    if request.method =='POST':
        try:

            nim = request.form['nim']
            q = Alumni.query.filter_by(nim=nim).first()
            if q.status == 'verified':
                flash_ = "Data anda sudah diverifikasi,Silahkan Login !"
                b = True
                return render_template('cek_status.html',flash_=flash_,b=b)
            else:
                flash_ = "Maaf, Data anda belum diverifikasi, mohon sabar menunggu..."
                b = False
                return render_template('cek_status.html',flash_=flash_,b=b)
                
        except :
            flash_= "Data anda tidak ditemukan !"
            b = False
            return render_template('cek_status.html',flash_=flash_,b=b)

    return render_template('cek_status.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('login'):
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['pass']
            if username == 'admin' and password == 'admin':
                session['user'] = 'admin'
                return redirect('/admin')
            try :
                q = User.query.filter_by(username=username).first()

                if check_password_hash(q.password,password):
                    if q.role == 0:
                        session['flash_l'] = 'Anda belum Terverifikasi, Mohon Tunggu verifikasi'
                        return redirect('/login')
                    else:
                        session['user'] =  q.username
                        return redirect('/')
                else:
                    session['flash_l'] = 'Anda salah memasukkan password ! '

                    return redirect('/login')
            except Exception as e :
                session['flash_l'] = f'{e}'
                return redirect('/login')
        flash_l = session.get('flash_l')
        return render_template('login.html',flash_l=flash_l)
@app.route('/registrasi',methods=['GET','POST'])
def daftar():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        email = request.form['email']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        agama = request.form['agama']
        alamat = request.form['alamat']
        tahun_lulus = request.form['tahun_lulus']
        ipk = request.form['ipk']
        judul_skripsi = request.form['judul_skripsi']
        pekerjaan = request.form['pekerjaan']
        tempat_bekerja = request.form['tempat_bekerja']
        foto = request.files['file']
        username = request.form['username']
        password  = generate_password_hash(request.form['password'])
        filename = secure_filename(foto.filename)
        try:
            foto.save(f'app/static/uploads/{filename}')
            q = Alumni(nama=nama,nim= nim,email=email,tempat_lahir=tempat_lahir,tanggal_lahir=tanggal_lahir,
            jenis_kelamin=jenis_kelamin,agama=agama,alamat=alamat,tahun_lulus=tahun_lulus,ipk=ipk,judul_skripsi=judul_skripsi,pekerjaan=pekerjaan,tempat_bekerja=tempat_bekerja,foto=filename,status='unverified'
            )

            b = User(nama=nama,username=username,password=password)
            db.session.add(q)
            db.session.add(b)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'{e}'
    return render_template('registrasi.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/user')
def user():
    if session.get('user') != 'admin':
        user = User.query.filter_by(username=session.get('user')).first()
        agenda = Agenda.query.first()
        return render_template('user/index.html',user=user,agenda=agenda)
    else:
        return redirect('/login')

@app.route('/user/<page>',methods=['GET','POST'])
def halaman(page):
    if session.get('user'):
        user = User.query.filter_by(username=session.get('user')).first()
        pekerjaan 
        if page == 'alumni':
            data = Alumni.query.all()
            jumlah = len(data)
            return render_template('user/alumni.html',user=user,alumni=data,jumlah=jumlah)
        elif page == 'pekerjaan': 
            data = pekerjaan.query.all()
            jumlah = len(data)
            return render_template('user/pekerjaan.html',user=user,data=data,jumlah=jumlah)


@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        return redirect('/login')
    else:
        alumni = len(Alumni.query.all())
        alumni_not_ver = len(Alumni.query.filter_by(status='unverified').all())
        alumni_ver = len(Alumni.query.filter_by(status='verified').all())

        
        data = {'total_alumni':alumni,'unverified':alumni_not_ver,'verified':alumni_ver,'pekerjaan':len(pekerjaan.query.all())}
        return render_template('admin/index.html',data=data)
    
    
@app.route('/admin/<page>')
def halaman_admin(page):
    if session.get('user') != 'admin':
        return redirect('/login')
    else:
        flas = session.get('flash_')
        if page == 'alumni':
            data = Alumni.query.all()
        elif page == 'pekerjaan':
            return redirect('/admin/pekerjaan/data/0')
        elif page == 'agenda':
            return redirect('/admin/agenda/data/0')
        elif page == 'user':
            data = User.query.all()
        return render_template(f'admin/{page}.html',data_alumni=data,flas=flas)




@app.route('/admin/alumni/<step>/<nim>',methods=['GET','POST'])
def alumni_(step,nim):
    if step == 'verifikasi':
        a = Alumni.query.filter_by(nim=nim).first()
        u = User.query.filter_by(nama=a.nama).first()
        a.status = "verified"
        u.role = 1
        session['flash_'] = f"{a.nama} Berhasil Di verifikasi !"
        db.session.commit()
        return redirect('/admin/alumni')
    elif step == 'tolak':
        a = Alumni.query.filter_by(nim=nim).first()
        u = User.query.filter_by(nama=a.nama).first()
        os.remove(f'app/static/uploads/{a.foto}')
        db.session.delete(a)
        db.session.delete(u)
        db.session.commit()
        session['flash_'] = f"{a.nama} Berhasil Di Hapus !"
        return redirect('/admin/alumni')
    elif step == 'add':
        if request.method == 'POST':
            nama = request.form['nama']
            nim = request.form['nim']
            email = request.form['email']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            agama = request.form['agama']
            alamat = request.form['alamat']
            tahun_lulus = request.form['tahun_lulus']
            ipk = request.form['ipk']
            judul_skripsi = request.form['judul_skripsi']
            pekerjaan = request.form['pekerjaan']
            tempat_bekerja = request.form['tempat_bekerja']
            foto = request.files['file']
            username = request.form['username']
            password  = generate_password_hash(request.form['password'])
            filename = secure_filename(foto.filename)
            try:
                foto.save(f'app/static/uploads/{filename}')
                q = Alumni(nama=nama,nim= nim,email=email,tempat_lahir=tempat_lahir,tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin,agama=agama,alamat=alamat,tahun_lulus=tahun_lulus,ipk=ipk,judul_skripsi=judul_skripsi,pekerjaan=pekerjaan,tempat_bekerja=tempat_bekerja,foto=filename,status='verified'
                )

                b = User(nama=nama,username=username,password=password)
                db.session.add(q)
                db.session.add(b)
                db.session.commit()
                session['flash_'] =  'Data Berhasil Ditambahkan'
                return redirect('/admin/alumni')
            except Exception as e:
                return f'{e}'
        return render_template('admin/add_alumni.html')
    elif step == 'edit':
        q = Alumni.query.filter_by(nim=nim).first()
        u = User.query.filter_by(nama=q.nama).first()
        if request.method == 'POST':
            nama = request.form['nama']
            q.nama = nama
            q.nim = request.form['nim']
            q.email = request.form['email']
            q.tempat_lahir = request.form['tempat_lahir']
            q.tanggal_lahir = request.form['tanggal_lahir']
            q.jenis_kelamin = request.form['jenis_kelamin']
            q.agama= request.form['agama']
            q.alamat= request.form['alamat']
            q.tahun_lulus = request.form['tahun_lulus']
            q.ipk = request.form['ipk']
            q.judul_skripsi = request.form['judul_skripsi']
            q.pekerjaan = request.form['pekerjaan']
            q.tempat_bekerja = request.form['tempat_bekerja']
            os.remove(f'app/static/uploads/{q.foto}')
            foto = request.files['file']
            filename = secure_filename(foto.filename)
            foto.save(f'app/static/uploads/{filename}')
            q.foto = filename
            u.nama = request.form['nama']
            u.username = request.form['username']
            u.password = generate_password_hash(request.form['password'])
            q.status = 'verified'
            db.session.commit()
            return redirect('/admin/alumni')
        return render_template('admin/edit_alumni.html',a=q,u=u)

            

@app.route('/admin/agenda/<step>/<id>',methods=['GET','POST'])
def agenda(step,id):
    data = Agenda.query.all()
    if step == 'hapus':
        q = Agenda.query.filter_by(id=id).first()
        os.remove(f'app/static/uploads/{q.banner}')
        db.session.delete(q)
        db.session.commit()
    
        return redirect('/admin/agenda/data/0')
    if step == 'data':
        if request.method == 'POST':
            try:
                title = request.form['judul']
                konten = request.form['isi']
                jadwal = request.form['jadwal']
                banner = request.files['file']
                banner.save(f'app/static/uploads/{banner.filename}')
                q = Agenda(title=title,konten=konten,jadwal=jadwal,banner=banner.filename)
                db.session.add(q)
                db.session.commit()
                return redirect('/admin/agenda/data/0')
            except Exception as e:
                return f'{e}'
        return render_template('admin/agenda.html',data=data)
    if step == 'edit':
        q = Agenda.query.filter_by(id=id).first()
        
        if request.method == 'POST':
            q.title = request.form['judul']
            q.konten = request.form['isi']
            q.jadwal = request.form['jadwal']
            os.remove(f'app/static/uploads/{q.banner}')
            banner = request.files['file']
            filename = secure_filename(banner.filename)
            q.banner = filename
            banner.save(f'app/static/uploads/{filename}')
            db.session.commit()
            return redirect('/admin/agenda/data/0')
        return render_template('/admin/agenda.html',data=data,q=q)
    

@app.route('/admin/pekerjaan/<step>/<id>',methods=['GET','POST'])
def loker(step,id):
    data = pekerjaan.query.all()
    if step == 'data':

        a = Alumni.query.all()
        email = []
        for i in a:
            email.append(i.email)

        if request.method == 'POST':
            try:
                perusahaan = request.form['perusahaan']
                lokasi = request.form['lokasi']
                job_title = request.form['job_title']
                deskripsi = request.form['desc_job']
                user_created = 'admin'
                q = pekerjaan(perusahaan=perusahaan,lokasi=lokasi,job_title=job_title,deskripsi=deskripsi)
                subject = f"Lowongan Pekerjaan -{job_title}-"
                body = f'{deskripsi}'
                send = send_notif(to=email,subject=subject,body=body)
                db.session.add(q)
                db.session.commit()
                if send :
                    session['SEND_MSG'] = "Sukses Mengirim Notif"
                else:
                    session['SEND_MSG'] = "GAGAL MENGIRIM NOTIF"


                    
                return redirect('/admin/pekerjaan')
            

            except Exception as e:
                return f'{e}'
        return render_template('admin/pekerjaan.html',data=data,msg=session.get('SEND_MSG'))
    if step == 'hapus':
        q = pekerjaan.query.filter_by(id=id).first()
        db.session.delete(q)
        db.session.commit()
        return redirect('/admin/pekerjaan')
    if step == 'edit':
        q = pekerjaan.query.filter_by(id=id).first()
        if request.method == 'POST':
            perusahaan = request.form['perusahaan']
            lokasi = request.form['lokasi']
            job_title = request.form['job_title']
            deskripsi = request.form['desc_job']
            q.perusahaan = perusahaan
            q.lokasi = lokasi
            q.job_title = job_title
            q.deskripsi = deskripsi
            db.session.commit()
            return redirect('/admin/pekerjaan')
        return render_template('admin/pekerjaan.html',data=data,u=q)
        

@app.route('/admin/excel/<page>')
def excel(page):
    if page == 'total_alumni':
        get_excel(page)
        return send_file(f'data/{page}.xlsx')
    elif page == 'alumni_verified':
        get_excel(page)
        return send_file(f'data/{page}.xlsx')
    elif page == 'alumni_unverified':
        get_excel(page)
        return send_file(f'data/{page}.xlsx')
    elif page == 'agenda':
        get_excel(page)
        return send_file(f'data/{page}.xlsx')
    elif page == 'pekerjaan':
        get_excel(page)
        return send_file(f'data/{page}.xlsx')






    
        




    
            

    
    


