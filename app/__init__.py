from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_restless import APIManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
# api_manager = APIManager(flask_sqlalchemy_db=db)
toolbar = DebugToolbarExtension()
lm = LoginManager()
lm.login_view = 'main.login'
 

def create_app(config_name, models={}):
    app = Flask(__name__)


    lm.init_app(app)
    
    
    User = models['User']
    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))
    


    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    # initialisation de l'api REST ==> ne fonctionne pas ...
    # api_manager.create_api(models['User'], methods=['GET', 'DELETE'])
    # api_manager.init_app(app)
    
    # initialisation de la barre de déboguage
    # toolbar.init_app(app)

    # Blueprint main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .csudadmin import csudadmin as csudadmin_blueprint
    app.register_blueprint(csudadmin_blueprint, url_prefix='/csudadmin')
    
    return app
    



