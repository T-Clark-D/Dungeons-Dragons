import csv
import os
from datetime import datetime

import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, render_template, flash, request
from forms import ContactForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm, ShippingForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(basedir, "data/characters.db")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/characters.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # returns in string form
    def __repr__(self):
        return '<Task %r>' % self.id


app.secret_key = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username, email, phone, password=None):
        self.id = username
        self.email = email
        self.phone = phone
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    with open('data/users.csv') as f:
        for user in csv.reader(f):
            if username == user[0]:
                return User(*user)
    return None


@app.route('/')
def index():
    with open('data/messages.csv') as f:
        doc_list = list(csv.reader(f))[1:]
    return render_template('base.html', username=session.get('username'), doc_list=doc_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted() and form.validate():
        user = find_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            flash('Logged in successfully.')
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/character_graveyard', methods=['POST', 'GET'])
@login_required
def c_g():
    if request.method == 'POST':
        character_content = request.form['content']
        new_character = Todo(content=character_content)

        try:
            db.session.add(new_character)
            db.session.commit()
            return redirect('/character_graveyard')
        except:
            return 'There was an issue adding your task'
    else:
        characters = Todo.query.order_by(Todo.date_created).all()
        return render_template('character_graveyard.html', characters=characters)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/character_graveyard')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/character_graveyard')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


@app.route('/roll_dice')
def r_d():
    return render_template('roll_dice.html')


@app.route('/external_resources')
def e_r():
    return render_template('external_resources.html')


@app.route('/player_leveling')
def p_l():
    with open('data/xpTable.csv') as f:
        doc_list = list(csv.reader(f))[1:]
    return render_template('player_leveling.html', doc_list=doc_list)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.is_submitted() and form.validate():
        with open('data/messages.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.email.data, form.message.data])
        return redirect(url_for('contact_response', name=form.name.data))
    return render_template('contact.html', form=form)


@app.route('/contact_response/<name>')
def contact_response(name):
    return render_template('contact_response.html', name=name)


@app.route('/merch')
def t():
    return render_template('merch.html')


@app.route('/shipping_info', methods=['POST'])
def s_i():
    form = request.form
    with open('data/shipping_info.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([form['First Name'], form['Last Name'], form['Email'], form['City'], form['State'], form['Zip code']])
    return render_template('shipping_info.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

print("don't worry, bout a thing cuz every little thing is gonna be alright, don't you worry!!!!")