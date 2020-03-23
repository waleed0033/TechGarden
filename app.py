from flask import Flask, render_template, flash, url_for, session, logging, request, redirect
from wtforms import Form, StringField, PasswordField, BooleanField, validators
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from passlib.hash import sha256_crypt
from datetime import timedelta
from flask_login import LoginManager
from functools import wraps


app = Flask(__name__)

#reCaptcha Google config
app.config['RECAPTCHA_PUBLIC_KEY']= '6LdWmOIUAAAAALBnW-byjnxFgGTN4otXh8dAc4sI'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdWmOIUAAAAAE2HuImf23hescbgdftadEv0T60P'
app.config['SECRET_KEY'] = 'DhI1U6g9Pv8wRCGakI3QTAlpWbG4'
app.config['TESTING'] = True

#configer timeout for the session
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=10)

app.config['MYSQL_HOST'] = '104.198.153.176'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'p364352951497-hkqqm8'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

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

class SingUpForm(Form):
    name = StringField('Name', validators=[validators.InputRequired(), validators.Length(min=2, max=50, message='Name must be between 2 and 50 characters long')])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Length(min=5,max=70, message='Email must be between 2 and 50 characters long'), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='password does not match'),
        validators.Length(min=6,max=50,message='Password must be between 6 and 50 characters long')
    ])
    confirm = PasswordField('Confirm Password',[validators.InputRequired()])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please Check the reCAPTCHA box")])


@app.route('/singup', methods=['get','post'])
def SingUp():
    form = SingUpForm(request.form)
    if request.method == 'POST' and form.validate():
        session['email'] = form.email.data
        session['password'] = form.password.data
        return redirect(url_for('dashboard'))
    
    return render_template('singup.html', form=form)

class Login(FlaskForm):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Length(min=5,max=70), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=6,max=50,message='Password must be between 6 and 50 characters long')
    ])
    rememberMe = BooleanField('Remember me')
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please Check the reCAPTCHA box")])

@app.route('/login', methods=['get','post'])
def login():
    form = Login(request.form)
    if form.validate_on_submit():
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

if __name__ == '__main__':
    app.run(debug=True)
