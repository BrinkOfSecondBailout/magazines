from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, magazine

@app.route('/new')
def add_new_mag():
    if not session:
        return redirect('/naughty')
    return render_template('add_new.html')


@app.route('/update_mag', methods=['POST'])
def update_mag():
    if not session:
        return redirect('/naughty')
    if not magazine.Magazine.validate_magazine(request.form):
        return redirect('/new')
    magazine.Magazine.add_new_magazine(request.form)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_one_magazine(id):
    if not session:
        return redirect('/naughty')
    data = {
        'magazine_id': id
    }
    return render_template('show_one.html', one_magazine=magazine.Magazine.show_one_magazine(data), all_subscribers=magazine.Magazine.get_all_subscribers_by_mag_id(data))

@app.route('/subscribe/<int:id>')
def add_subscriber(id):
    if not session:
        return redirect('/naughty')
    data = {
        'subscriber_id': session['user_id'],
        'magazine_id': id
    }
    magazine.Magazine.add_subscriber(data)
    data1 = {
        'magazine_id': id
    }
    magazine.Magazine.update_subscriber_count(data1)
    return redirect('/dashboard')

@app.route('/destroy/<int:id>')
def destroy_magazine(id):
    if not session:
        return redirect('/naughty')
    data = {
        'magazine_id': id
    }
    if not magazine.Magazine.validate_matching_id(data):
        return redirect('/naughty')
    magazine.Magazine.disable_foreign_key()
    magazine.Magazine.destroy_magazine(data)
    user_id = session['user_id']
    return redirect(f'/account/{user_id}')