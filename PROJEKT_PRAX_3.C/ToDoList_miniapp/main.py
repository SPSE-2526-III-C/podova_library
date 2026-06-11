from flask import Flask, json, render_template, redirect, url_for, request, flash, session, request
import os, smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random


from extensions import db
from models import User, SavedBook
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
    app.run(debug=True)


with app.app_context():
    db.create_all()

@app.route('/base')
def base():
    return render_template('index.html')

@app.route('/') 
def home_page():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        
        meno = request.form.get('name')
        uzivatel_email = request.form.get('email')
        sprava = request.form.get('message')

        
        msg = EmailMessage()
        msg['Subject'] = f"Nová správa od: {meno}"
        msg['From'] = EMAIL_ADRESA
        msg['To'] = EMAIL_ADRESA  # Správa príde mne
        msg['Reply-To'] = uzivatel_email
        msg.set_content(f"Meno: {meno}\nE-mail: {uzivatel_email}\n\nSpráva:\n{sprava}")

        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADRESA, EMAIL_HESLO)
                smtp.send_message(msg)
            flash("Message was sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {e}", "error")

        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/hladaj', methods=['GET', 'POST'])
def hladaj():
    kniha_nazov = request.form.get('kniha').lower()
    TESTOVACI_REŽIM = False
    
    if not kniha_nazov:
        return redirect(url_for('base'))
    elif request.method == 'POST':
        
        if TESTOVACI_REŽIM:
            with open('test.json', encoding='utf-8') as f:
                vsetky_data = json.load(f)
            vysledok = []
            for kniha in vsetky_data.get('items', []):
                nazov_knihy = kniha['volumeInfo'].get('title', '').lower()
                autor_knihy = kniha['volumeInfo'].get('authors', '').lower()
                if kniha_nazov in nazov_knihy or kniha_nazov in autor_knihy:
                    vysledok.append(kniha)

                
        
            data = {'items': vysledok}
    
        elif kniha_nazov:
            kniha_nazov = request.form.get('kniha')
            url = f"https://www.googleapis.com/books/v1/volumes?q={kniha_nazov}&key=AIzaSyD9Iow9WEZqUV4-h65XYSs6YHZ-LPfvT1w"
            print(url)
            response = requests.get(url)
            data = response.json()
            print(data)

    
        
    return render_template('vysledky.html', knihy = data.get('items', []))


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
            session['user_id'] = query_user.id
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
            flash("Registraision success! Please log in", "success")
            return redirect(url_for('login'))
        
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
    

@app.route('/vysledky')
def vysledky():
    kniha_nazov = (request.form.get('kniha')or "").lower()
    TESTOVACI_REŽIM = False
    
    if not kniha_nazov:
        return redirect(url_for('base'))
    elif request.method == 'POST':
        
        if TESTOVACI_REŽIM:
            with open('test.json', encoding='utf-8') as f:
                vsetky_data = json.load(f)
            vysledok = []
            for kniha in vsetky_data.get('items', []):
                nazov_knihy = kniha['volumeInfo'].get('title', '').lower()
                autor_knihy = kniha['volumeInfo'].get('authors', '').lower()
                if kniha_nazov in nazov_knihy or kniha_nazov in autor_knihy:
                    vysledok.append(kniha)

            data = {'items': vysledok}
            print(data)
    
        elif kniha_nazov:
            kniha_nazov = request.form.get('kniha')
            url = f"https://www.googleapis.com/books/v1/volumes?q={kniha_nazov}&key=AIzaSyD9Iow9WEZqUV4-h65XYSs6YHZ-LPfvT1w"
            print(url)
            response = requests.get(url)
            data = response.json()
            print(data)

        
    return render_template('vysledky.html', knihy = data.get('items', []))


@app.route('/description/<kniha_id>', methods = ['GET', 'POST'])
def description(kniha_id):
    TESTOVACI_REŽIM = False
    vysledok = []
    if kniha_id: 
        
        if TESTOVACI_REŽIM:
            with open('test.json', encoding='utf-8') as f:
                data = json.load(f)
            for kniha in data.get('items', []):
                if kniha['id'] == kniha_id:
                    vysledok.append(kniha)
            data = {'items': vysledok}

        else:
            url = f"https://www.googleapis.com/books/v1/volumes/{kniha_id}?key=AIzaSyD9Iow9WEZqUV4-h65XYSs6YHZ-LPfvT1w"
            print(url)
            response = requests.get(url)
            data = response.json()

    else:
        flash("Book was not found")
        return redirect(url_for('base'))
    
    if data.get('items'):
        kniha_pre_html = data['items'][0]
    elif 'volumeInfo' in data:
        kniha_pre_html = data
    else:
        kniha_pre_html = None
    
    if request.method == 'POST':
        user_id = session.get('user_id')
        
        if kniha_pre_html:
            nazov_kniha = kniha_pre_html['volumeInfo']['title']
            ulozena = SavedBook.query.filter_by(user_id=user_id, book_title=nazov_kniha).first()
            if ulozena:
                flash("this book is already saved", "error")
                return redirect(url_for('description', kniha_id=kniha_id))
            else:
                nova_kniha = SavedBook(book_title = nazov_kniha, user_id = user_id)
                db.session.add(nova_kniha)
                db.session.commit()
                return redirect(url_for('profile', user_id=user_id))
        else:
            flash("Cannot save an invalid book")
            return redirect(url_for('rec'))

    return render_template('description.html', kniha=kniha_pre_html)


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if 'logged_in' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login'))
        
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for('base'))
        
    # zmena fotky
    if request.method == 'POST':
        novy_avatar = request.form.get('vybrany_avatar')
        if novy_avatar:
            user.photo = novy_avatar
            db.session.commit()
            
        
        return redirect(url_for('profile', user_id=user_id))

    #vykreslenie profilu
    username = user.username
    photo = user.photo
    my_book = SavedBook.query.filter_by(user_id=user_id).all()
    
    
    return render_template('profile.html', username=username, photo=photo, my_book=my_book, user_id=user_id)

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    kniha = SavedBook.query.get(book_id)
    db.session.delete(kniha)
    db.session.commit()
    user_id = session.get('user_id')
    return redirect(url_for('profile', user_id = user_id))

@app.route('/update_book/<int:book_id>', methods=['GET','POST'])
def update_book(book_id):
    
    rating = request.form.get('rating')
    notes = request.form.get('notes')
    reading_status = request.form.get('status')
    kniha = SavedBook.query.get(book_id)
    kniha.rating =  rating
    kniha.notes = notes
    kniha.reading_status = reading_status
    db.session.commit()
    return redirect(url_for('profile', user_id = kniha.user_id))

@app.route('/rec', methods=['GET','POST'])
def rec():
    TESTOVACI_REZIM = False
    if not 'logged_in' in session:
        flash("Invalid request. Please log in first", 'error')
        return redirect(url_for('login'))
    
    if 'logged_in' in session:
        user_id = session.get('user_id')
        moje_knihy = SavedBook.query.filter_by(user_id=user_id).all()
        hladany_vyraz = "bestsellers"
        if moje_knihy:
            hladany_vyraz= random.choice(moje_knihy).book_title
        else:
            hladany_vyraz= hladany_vyraz
        if TESTOVACI_REZIM:
            with open('test.json', encoding='utf-8') as f:
                data = json.load(f)
                odporucane = []
                for kniha in data.get('items', []):
                    if hladany_vyraz.lower() in kniha['volumeInfo'].get('title','').lower():
                        odporucane.append(kniha)
                if not odporucane:
                    odporucane=data.get('items',[])[:5]
                    data = {'items': odporucane}
        else:
            url = f"https://www.googleapis.com/books/v1/volumes?q={hladany_vyraz}&key=AIzaSyD9Iow9WEZqUV4-h65XYSs6YHZ-LPfvT1w"
            response = requests.get(url)
            data = response.json()

        return render_template('rec.html', knihy=data.get('items',[]), podla_knihy = hladany_vyraz)