import unittest
from flask import request, make_response, redirect, render_template, session, flash, url_for
from flask_login import login_required, current_user

from app import create_app
from app.forms import TodoForm
from app.firestore_service import get_todos, create_todo

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def home():
    user_ip = request.remote_addr
    response = make_response(redirect('/ip'))
    session['user_ip'] = user_ip
    return response

@app.route('/ip', methods=['GET', 'POST'])
@login_required
def ip():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
    }

    if todo_form.validate_on_submit():
        description = todo_form.description.data

        create_todo(user_id=username, description=description)

        flash('Tarea creada')
        return redirect(url_for('ip'))

    return render_template('ip.html', **context)
