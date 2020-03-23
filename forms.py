from wtforms import StringField, PasswordField, BooleanField, validators
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm


class Login(FlaskForm):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Length(min=5,max=70), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=6,max=50,message='Password must be between 6 and 50 characters long')
    ])
    rememberMe = BooleanField('Remember me')
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please Check the reCAPTCHA box")])

class SingUpForm(FlaskForm):
    name = StringField('Name', validators=[validators.InputRequired(), validators.Length(min=2, max=50, message='Name must be between 2 and 50 characters long')])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Length(min=5,max=70, message='Email must be between 2 and 50 characters long'), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='password does not match'),
        validators.Length(min=6,max=50,message='Password must be between 6 and 50 characters long')
    ])
    confirm = PasswordField('Confirm Password',[validators.InputRequired()])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please Check the reCAPTCHA box")])