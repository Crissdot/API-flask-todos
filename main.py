from flask import request, make_response, redirect, render_template, session
import unittest

from app import create_app
from app.forms import LoginForm

app = create_app()

todos = ['TODO1', 'TODO2', 'TODO3', 'TODO4', 'TODO5']



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
        'todos': todos,
        'username': username,
    }

    return render_template('ip.html', **context)
