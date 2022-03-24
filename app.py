from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
from sqlalchemy import inspect
import secrets
db = SQLAlchemy()
def create_app():
    app = Flask(__name__, template_folder='templates')
    secret_key = secrets.token_urlsafe(16)
    app.config['SECRET_KEY'] = secret_key
    #modifique com o 'tipo+conexão://user:senha@local/nomedatabase' do banco de dados
    tipo="postgresql"
    conexao="psycopg2"
    user="postgres"
    password="123456789"
    local="localhost"
    dbname="servidor_agenda"
    app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}/{}'.format(tipo,conexao,user,password,local,dbname)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456789@localhost/servidor_agenda'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from auth import auth as auth_blueprint
    from agenda import agenda as agenda_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(agenda_blueprint)
    app.register_blueprint(main_blueprint)
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id)) 
    return app
class Usuario(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    login = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100),nullable=False)
    nome = db.Column(db.String(100),nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
class Agenda(db.Model):
    id= db.Column(db.Integer,primary_key=True) 
    nome= db.Column(db.String(100),nullable=False)
    telefone= db.Column(db.String(14),nullable=False)
    email= db.Column(db.String(100),nullable=False)
    dono_id=db.Column(db.Integer,db.ForeignKey('usuario.id'))
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
class Pesquisa(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    dono_id=db.Column(db.Integer,db.ForeignKey('usuario.id'))
    letra=db.Column(db.String(1),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }