from flask import Blueprint

main = Blueprint('main', __name__, template_folder="templates/main")

from . import views, errors
