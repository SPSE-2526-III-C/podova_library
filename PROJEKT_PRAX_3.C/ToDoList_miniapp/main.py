from flask import Flask, render_template, redirect, url_for, request, flash, redirect
from forms import KorculovanieForm
from models import db, Pridaj
import os, smtplib
from email.message import EmailMessage

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sigma67'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "korculovanie.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "nejake_tajne_heslo"

# Konfigurácia e-mailu (Príklad pre Gmail)
EMAIL_ADRESA = "booksofyourdreams123@gmail.com"
EMAIL_HESLO = "olpq qdxc rics ovsu"

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 1. Získanie dát z formulára
        meno = request.form.get('name')
        uzivatel_email = request.form.get('email')
        sprava = request.form.get('message')

        # 2. Príprava e-mailu
        msg = EmailMessage()
        msg['Subject'] = f"Nová správa od: {meno}"
        msg['From'] = EMAIL_ADRESA
        msg['To'] = EMAIL_ADRESA  # Správa príde tebe
        msg['Reply-To'] = uzivatel_email
        msg.set_content(f"Meno: {meno}\nE-mail: {uzivatel_email}\n\nSpráva:\n{sprava}")

        # 3. Reálne odoslanie
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADRESA, EMAIL_HESLO)
                smtp.send_message(msg)
            flash("Správa bola úspešne odoslaná!", "success")
        except Exception as e:
            flash(f"Chyba pri odosielaní: {e}", "danger")
            
        return redirect(url_for('contact'))
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

