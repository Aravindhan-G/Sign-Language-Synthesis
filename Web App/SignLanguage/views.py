from flask import Blueprint, render_template, request,flash,redirect,url_for
from . import c,conn

views= Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user = request.form.get('user')
        passw = request.form.get('pass')
        c.execute("SELECT * FROM LOGIN WHERE Name = '%s'"%(user))
        data = c.fetchone()
        if data:
            if len(data)!=0:
                if passw==data[2]:
                    flash("Logged In successfully", category='success')
                    return redirect(url_for('detect.home'))
                else:
                    flash('Incorrect Password', category='error')
                    return render_template('home.html')
        else:
            flash("User Name Doesn't Exist", category='error')
            return render_template('home.html')  
    return render_template('home.html')

@views.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('user')
        mail = request.form.get('mail')
        pass1 = request.form.get('pass')
        pass2 = request.form.get('pass1')
        c.execute("SELECT * FROM LOGIN WHERE Name = '%s'"%(name))
        data = c.fetchall()
        if len(data) == 0:
            if not pass1 == pass2:
                flash("Password Din't Match", category='error')
                return render_template('signup.html')
            else:
                c.execute("INSERT INTO LOGIN VALUES('%s','%s','%s','%s')"%(name,mail,pass1,pass2))
                flash("Sign Up Successful", category='success')
                return render_template('home.html')
        else:
            flash("User Name Already Exist", category='error')
            return render_template('signup.html')
    return render_template('signup.html')