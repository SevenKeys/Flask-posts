from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from passlib.hash import sha256_crypt
from functools import wraps

from user_posts.data.models import Author, db
from user_posts.auth.forms import RegisterForm

admin = Blueprint('admin', __name__, template_folder='templates')

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' not in session:
            flash('You need login first to see this page')
            return redirect(url_for('admin.login'))
        return func(*args,**kwargs)
    return wrapper

@admin.route('/authors')
@login_required
def display_authors():
    authors = [author for author in Author.query.all()]
    return render_template('authors.html', authors=authors)

@admin.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            user = Author.query.filter(Author.username == username).first()
            if not user:
                author = Author(username=username, email=email, password=password)
                db.session.add(author)
                db.session.commit()
                flash('Congratulations, you are registered!')
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('admin.display_authors'))
            else:
                flash('You should choose another username')
    except Exception as e:
        return 'Error: ',e
    return render_template('register.html', form=form)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            enter_username = request.form['username']
            enter_password = request.form['password']
            user = Author.query.filter(Author.username == enter_username).first()
            if user:
                db_pass = user.password
                if sha256_crypt.verify(enter_password, db_pass):
                    session['logged_in'] = True
                    session['username'] = enter_username
                    flash('You are logged in!')
                    return redirect(url_for('main.display_posts'))
                else:
                    error = 'Invalid password'
            else:
                error = 'Invalid username'
        except Exception as e:
            flash(e)
    return render_template('login.html', error=error)

@admin.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    flash('You are logout')
    return redirect(url_for('main.index'))

@admin.route('/delete/<int:user_id>', methods=['GET'])
def delete(user_id):
    try:
        user = Author.query.filter(Author.id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('You are successfully deleted')
    except Exception as e:
        flash(e)
    return redirect(url_for('admin.logout'))