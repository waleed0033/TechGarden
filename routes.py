from flask import render_template, flash, url_for, request, redirect, session
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from flask import render_template
from functools import wraps
from forms import *
from app import app

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/singup', methods=['get','post'])
def SingUp():
    form = SingUpForm(request.form)
    if request.method == 'POST' and form.validate():
        session['email'] = form.email.data
        session['password'] = form.password.data
        return redirect(url_for('dashboard'))
    
    return render_template('singup.html', form=form)

@app.route('/login', methods=['get','post'])
def login():
    form = Login(request.form)
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.email.data, form.rememberMe.data),'success')
        if form.rememberMe.data == True:
            session['_permanent'] = True

        session['email'] = form.email.data
        session['password'] = form.password.data
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
@is_logged_in
def profile():
    return render_template('profile.html')