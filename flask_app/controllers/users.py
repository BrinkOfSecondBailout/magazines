from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, magazine
bcrypt = Bcrypt(app)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/process/registration', methods=['POST'])
def process_registration():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user.User.save_user(data)
        return redirect('/')


@app.route('/process/login', methods=['POST'])
def process_login():
    user1 = user.User.validate_login(request.form)
    if not user1:
        return redirect('/')
    if not bcrypt.check_password_hash(user1['password'], request.form['password']):
        flash('Incorrect password! Try again.', 'login')
        return redirect('/')
    else:
        session['user_id'] = user1['id']
        return redirect('/dashboard')

@app.route('/dashboard')
def show_dashboard():
    if not session:
        return redirect('/naughty')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user_info=user.User.get_info_by_id(data), all_magazines=magazine.Magazine.show_all_magazines())

@app.route('/account/<int:id>')
def show_account_page(id):
    if not session:
        return redirect('/naughty')
    if session['user_id'] != id:
        return redirect('/naughty')
    data = {
        'id': id
    }
    return render_template('account.html', user_info=user.User.get_info_by_id(data), all_magazines=magazine.Magazine.get_all_magazines_by_user(data))

@app.route('/update_account/<int:id>', methods=['POST'])
def update_account(id):
    if not session:
        return redirect('/naughty')
    if session['user_id'] != id:
        return redirect('/naughty')
    user.User.validate_edit(request.form)
    user.User.update_user(request.form)
    return redirect(f'/account/{id}')

@app.route('/naughty')
def naughty_hacker():
    return render_template('naughty.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
