from flask import request, make_response, redirect, render_template, session
import unittest

from app import create_app
from app.firestore_service import get_users, get_todos

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

@app.route('/ip')
def ip():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
    }

    users = get_users()

    for user in users:
        print(user.to_dict())

    return render_template('ip.html', **context)
