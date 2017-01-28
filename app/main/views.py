from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main


@main.route('/')
def index():
    return render_template('index.html', message="Ravis de vous revoir")

@main.route('/sql', methods=['GET', 'POST'])
def sql():
    query = "SELECT * FROM users LIMIT 10;"
    return render_template('sql.html', sql=query)
    