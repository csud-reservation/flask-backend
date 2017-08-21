from flask import Blueprint

sendmail = Blueprint('sendmail', __name__, template_folder='templates/sendmail')

from . import views
