from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import Usuario,db
#carrega flask e Agenda
auth = Blueprint('auth',__name__,url_prefix="/auth")
#rotas da aplicação
@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('email')
    senha = request.form.get('senha')
    remember = True if request.form.get('remember') else False
    #s="select login,senha from Usuário where usuário.login= '"+login+"' and usuário.senha='"+senha+"'"  
    #r=consultar_db(s)
    user=Usuario.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.senha,senha):
        flash('Verifique seu login e tente de novo')
        return redirect(url_for('auth.login'))
    login_user(user,remember=remember)
    return redirect(url_for('main.profile'))
@auth.route('/signup')
def signup():
    return render_template('signup.html')
@auth.route('/signup1',methods=['POST'])
def signup_post():
    login= request.form.get('email')
    nome=request.form.get('nome')
    senha= request.form.get('senha')
    #s="select login from Usuário where usuário.login= '"+login+"'"
    #r=consultar_db(s)
    user = Usuario.query.filter_by(login=login).first()
    if user:
        flash('Já existe esse email. Tente logar!')
        return redirect(url_for('auth.signup'))
    #novo_user="insert into Usuário(login,senha) values('{}','{}') on conflict do nothing;".format(login,senha)
    #inserir_na_tabela(novo_user)
    novo_usuario = Usuario(login=login, nome=nome, senha=generate_password_hash(senha, method='sha256'))
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('auth.login'))
@auth.route('/logout')
def logout():
    logout_user()
    flash("Deslogou de profile")
    return redirect(url_for('main.home'))
