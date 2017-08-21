from flask import Blueprint

csudadmin = Blueprint('csudadmin', __name__, template_folder='templates/csudadmin')

from . import views
