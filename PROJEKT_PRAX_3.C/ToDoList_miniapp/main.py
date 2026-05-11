from flask import Flask, render_template, redirect, url_for
from forms import KorculovanieForm
from models import db, Pridaj
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sigma67'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "korculovanie.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/') 
def home_page():
    return render_template('index.html')

@app.route('/pridaj_ulohu', methods=['GET', 'POST'])
def pridaj_ulohu():
    form = KorculovanieForm()
    if form.validate_on_submit():
        novy_zaznam = Pridaj(
            nazov=form.nazov.data,
            ohodnot=form.ohodnot.data,
            teren=form.teren.data,
            pocasie=form.pocasie.data,
            popis=form.popis.data
        )
        db.session.add(novy_zaznam)
        db.session.commit()
        return redirect(url_for('pridaj_ulohu'))
    return render_template('pridaj_ulohu.html', form=form)

@app.route('/zaznam')
def zaznam():
    korc = Pridaj.query.order_by(Pridaj.datum_pridania.desc()).all()
    return render_template('zaznam.html', korc=korc)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
