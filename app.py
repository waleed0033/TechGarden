from flask import Flask, render_template, flash, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_wtf import RecaptchaField, Recaptcha
from passlib.hash import sha256_crypt

app = Flask(__name__)

#reCaptcha Google config
app.config['RECAPTCHA_PUBLIC_KEY']= '6LdWmOIUAAAAALBnW-byjnxFgGTN4otXh8dAc4sI'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdWmOIUAAAAAE2HuImf23hescbgdftadEv0T60P'
app.config['SECRET_KEY'] = 'DhI1U6g9Pv8wRCGakI3QTAlpWbG4'
app.config['TESTING'] = True

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
        return request.values
    
    return render_template('singup.html', form=form)

class Login(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Length(min=5,max=70), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=6,max=50,message='Password must be between 6 and 50 characters long')
    ])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please Check the reCAPTCHA box")])

@app.route('/login', methods=['get','post'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        return request.values
    
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
