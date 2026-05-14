from flask import Flask, render_template, redirect, url_for, request, flash, session
import os, smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash

# 1. IMPORTUJ DB A MODELY (Pridaj aj 'Pridaj', ak ho tam máš)
from extensions import db
from models import User
from forms import KorculovanieForm

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sigma67'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Bubble"
db.init_app(app)
app

# E-mail
EMAIL_ADRESA = "booksofyourdreams123@gmail.com"
EMAIL_HESLO = "olpq qdxc rics ovsu"

if __name__ == '__main__':
    app.app_context().push()
    app.debug = True
    db.create_all()
    app.secret_key="Bubble"
    app.run(host='127.0.0.1', port=5000)


with app.app_context():
    db.create_all()

@app.route('/') 
def home_page():
    return render_template('index.html')

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
            flash("Message was sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {e}", "error")

        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/books')
def books():
    return render_template('books.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query_user = User.query.filter_by(email=email).first()
        

        if not email and not password:
            flash("Please fill in all fields", "error")
            return redirect(url_for('login'))
        
        elif query_user and check_password_hash(query_user.password, password):
            session['logged_in'] = True
            return redirect(url_for('base'))
        
        else:
            
            flash("Wrong email or password. Please try again", "error")
            return redirect(url_for('login'))
    
    
    
    elif 'logged_in' in session:
        flash("You are logged in. Log out first to log in with a different account.", "error")
        return redirect(url_for('logout'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        if existing_user or existing_username:
            flash("Email or username already exists. Please choose another", "error")
            return redirect(url_for('register'))
        else:
            new_user = User(
                username = request.form['username'],
                email = request.form['email'],
                password=generate_password_hash(request.form['password'])
            )
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('base'))
        
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])

def logout():
    if request.method == 'POST':
        if 'logged_in' in session:
            session.clear()
            
            return redirect(url_for('base'))
        else:
            flash("Invalid request. Please log in first", "error")
            return redirect(url_for('login'))
        
    elif 'logged_in' not in session:
        flash("Invalid request. Please log in first", "error")
        return redirect(url_for('login'))

 

    return render_template('logout.html')
    