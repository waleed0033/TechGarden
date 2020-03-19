from flask import Flask, render_template, flash, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

class SingUpForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)], validators.)
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Email("please enter val"), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/singup', methods=['get','post'])
def SingUp():
    form = SingUpForm(request.form)
    return render_template('singup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
