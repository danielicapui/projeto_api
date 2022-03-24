from flask import Flask,render_template,Blueprint
from flask_login import login_required,current_user
from app import create_app,Pesquisa,db
main= Blueprint("main",__name__,url_prefix="/main")
@main.route('/home')
def home():
    return render_template('base.html')
@main.route('/profile')
@login_required
def profile():
    pesquisa=Pesquisa.query.filter_by(dono_id=current_user.id).first()
    if pesquisa:
        r=Pesquisa.query.get(pesquisa.id)
        r.letra="A"
        db.session.commit()
    else:
        nova_pesquisa=Pesquisa(letra='A',dono_id=current_user.id)
        db.session.add(nova_pesquisa)
        db.session.commit()
    return render_template('profile.html',nome=current_user.nome)
if __name__=="__main__":
    ap=create_app()
    ap.run(debug = False,host="0.0.0.0")