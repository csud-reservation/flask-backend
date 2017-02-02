from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length

class LoginForm(Form):
    account = StringField("Nom d'utilisateur" ,validators=[Required()], render_kw={"placeholder": "Sigle ou adresse edufr"})
    password = PasswordField("Mot de passe",validators=[Required()], render_kw={"placeholder": "Mot de passe"})
    remember_me = BooleanField('Se rappeler de moi')
    submit = SubmitField('Se connecter')
    
    
class ChangePasswordForm(Form):
    old_pw = PasswordField("Mot de passe actuel",validators=[Required()], render_kw={"placeholder": 'Mot de passe actuel'})
    new_pw = PasswordField("Nouveau mot de passe",validators=[Required(), Length(8,128)], render_kw={"placeholder": 'Nouveau mot de passe'})
    new_pw2 = PasswordField("Confirmation du nouveau mot de passe",validators=[Required(), Length(8,128)], render_kw={"placeholder": 'Confirmation du nouveau mot de passe'})
    modify = SubmitField('Modifier')