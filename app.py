from flask import Flask, render_template, flash, url_for, logging, request, redirect
from wtforms import Form, StringField, PasswordField, BooleanField, validators
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from passlib.hash import sha256_crypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile('config.py')

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
