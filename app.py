from flask import Flask, render_template, flash, url_for, session, logging, request, redirect
from wtforms import Form, StringField, PasswordField, BooleanField, validators, ValidationError
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from passlib.hash import sha256_crypt
from datetime import timedelta
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import pymysql
from datetime import datetime
import pygal
from timeago import format

pymysql.install_as_MySQLdb()

app = Flask(__name__)

#reCaptcha Google config
app.config['RECAPTCHA_PUBLIC_KEY']= '6LdWmOIUAAAAALBnW-byjnxFgGTN4otXh8dAc4sI'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdWmOIUAAAAAE2HuImf23hescbgdftadEv0T60P'
app.config['SECRET_KEY'] = 'DhI1U6g9Pv8wRCGakI3QTAlpWbG4'
app.config['TESTING'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://0vrp4Gz4RM:I2EQa4FkfT@remotemysql.com:3306/0vrp4Gz4RM?charset=utf8mb4'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask:I2EQa4FkfT@104.198.153.176/techgarden'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login = LoginManager(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
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

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')    

@app.route('/singup', methods=['get','post'])
def SingUp():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SingUpForm(request.form)
    if form.validate_on_submit():
        user = User(name = form.name.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user!','success')
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = Login(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password','danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.rememberMe.data)
        flash('Welcome ' + current_user.name + ' you have login successfully ' ,'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['get','post'])
@is_logged_in
def dashboard():
    for garden in current_user.gardens:
        if garden.lastRecoerd().temperature < garden.have.Min_Temp:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in temperature below than ' + str(garden.have.Min_Temp),'danger')
        elif garden.lastRecoerd().temperature > garden.have.Max_Temp:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in temperature higher than ' + str(garden.have.Max_Temp),'danger')
        elif garden.lastRecoerd().humidity < garden.have.Min_Hum:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in humidity below than ' + str(garden.have.Min_Hum) + '%','danger')
        elif garden.lastRecoerd().humidity > garden.have.Max_Hum:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in humidity higher than ' + str(garden.have.Max_Hum) + '%','danger')
        elif garden.lastRecoerd().soil_moist < garden.have.Min_S_Moist:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in Soil Moist below than ' + str(garden.have.Min_S_Moist) + '%','danger')
        elif garden.lastRecoerd().soil_moist > garden.have.Max_S_Moist:
            flash('Warning : Garden ' + garden.name + ' have ' + garden.have.name + ' plant where this plant cannot grow in Soil Moist higher than ' + str(garden.have.Max_S_Moist) + '%','danger')

    if request.method == 'POST':
        garden_id = request.form['id']
        gardenNew = Garden.query.filter_by(id=garden_id).first()
        if gardenNew is not None:
            if gardenNew.owner is not None:
                flash('fail' ,'danger')
            else:
                gardenNew.owner = current_user
                db.session.commit()
                flash('You have add successfully ' ,'success')

    return render_template('dashboard.html')

@app.route('/esp',methods=['post'])
def arduino():
    garden_id = request.form['garden_id']
    humidity = request.form['humidity']
    temperature = request.form['temperature']
    water_level = request.form['water_level']
    soil_moist = request.form['soil_moist']
    water_pump = request.form['water_pump']
    record = Record(garden_id=garden_id, humidity=humidity, temperature=temperature, water_level=water_level, soil_moist=soil_moist, water_pump=water_pump)
    db.session.add(record)
    db.session.commit()

    return 'OK,' + Plant.Min_Hum + ',' + Plant.Max_Hum

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logout successfully ' ,'success')
    return redirect(url_for('login'))

@app.route('/profile')
@is_logged_in
def profile():
    return render_template('profile.html')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gardens = db.relationship('Garden', backref='owner',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    Min_Hum = db.Column(db.Integer)
    Max_Hum = db.Column(db.Integer)
    Min_Temp = db.Column(db.Integer)
    Max_Temp = db.Column(db.Integer)
    Min_S_Moist = db.Column(db.Integer)
    Max_S_Moist = db.Column(db.Integer)
    gardens = db.relationship('Garden', backref='have')

    def __repr__(self):
        return '<Plant {}>'.format(self.id)

class Garden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    records = db.relationship('Record', backref='records')

    def __repr__(self):
        return '<Garden {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def lastRecoerd(self):
        return Record.query.filter_by(garden_id=self.id).order_by(desc(Record.id)).first()        

    def lastFiveRecoerd(self):
        recoerds = Record.query.filter_by(garden_id=self.id).order_by(desc(Record.id)).limit(15)
        timestamp = []
        temperature = []
        humidity = []
        soil_moist = []
        water_level = []

        for recoerd in recoerds:
            timestamp.insert(0,recoerd.timestamp.strftime('%H:%M'))
            temperature.insert(0,recoerd.temperature)
            humidity.insert(0,recoerd.humidity)
            soil_moist.insert(0,recoerd.soil_moist)
            water_level.insert(0,recoerd.water_level)

        graph = pygal.Line()
        graph.title = 'Graph to show the change of time and other variables'
        graph.x_labels = timestamp
        graph.add('Temperature', temperature)
        graph.add('Humidity', humidity)
        graph.add('Soil Moist', soil_moist)
        graph.add('Water Level', water_level)
        graph_data = graph.render_data_uri()
        return graph_data

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    garden_id = db.Column(db.Integer, db.ForeignKey('garden.id'))
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    water_level = db.Column(db.Integer)
    soil_moist = db.Column(db.Integer)
    water_pump = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Record {}>'.format(self.id)

@app.route('/remove/<int:remove_garden_id>')
@is_logged_in
def removeGarden(remove_garden_id):
    checkifremoved = False
    for gardenRemove in current_user.gardens:
        if gardenRemove.id == remove_garden_id:
            gardenRemove.user_id = None
            db.session.add(gardenRemove)
            db.session.commit()
            checkifremoved = True
            break
    
    if checkifremoved:
        flash('The garden have been removed successfully','success')
    else:
        flash('Fail to remove the garden','danger')
    
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')