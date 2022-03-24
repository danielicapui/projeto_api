import email
from flask import Flask,render_template,request,Blueprint,redirect,url_for,flash
from flask_login import login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask.json import jsonify
from utills import *
from app import db,Usuario,Agenda,Pesquisa
import json
#carrega flask e Agenda
agenda = Blueprint('agenda',__name__,url_prefix="/agenda")
agenda_db=Agenda()
#rotas da agenda
@agenda.route('/index',methods=['GET'])
@login_required
def index():
    return render_template('index.html')
@agenda.route('/consultar_letra',methods=['GET','POST'])
@login_required
def consulta_por_letra():
    if request.method=='POST':
        letra=request.form.get('letra')
        letra=letra.lower()
        #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
        r=Agenda.query.filter(Agenda.nome.ilike(letra+"%"),Agenda.dono_id==current_user.id)
        if letra in string.ascii_lowercase:
            p=Pesquisa.query.filter_by(dono_id=current_user.id).first()
            search=Pesquisa.query.get(p.id)
            search.letra=letra
            db.session.commit()
        if r:
            return jsonify(handle_agenda(r))
        else:
            flash("Nenhum resultado encontrado")
            return redirect(url_for('agenda.consulta_por_letra'))
    #r=tratar_tuplas(registro)
    elif request.method=='GET':
        return render_template('consultar_letra.html')
@agenda.route('/consultar_nome',methods=['GET','POST'])
@login_required
def consulta_por_nome():
    if request.method=='POST':
            nome=request.form.get('nome')
            #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
            r=Agenda.query.filter(Agenda.nome.ilike(nome.lower()),Agenda.dono_id==current_user.id)
            if r: 
                return jsonify(handle_agenda(r))
            else:
                flash("Nenhum resultado encontrado")
                return redirect(url_for('agenda.consulta_por_letra'))
        #r=tratar_tuplas(registro)
    elif request.method=='GET':
            return render_template('consultar_nome.html')
    return r
@agenda.route('/retornar_registro',methods=['GET','POST'])
@login_required
def proximo_registro():
    if request.method=='POST':
            id=request.form.get('id')
            #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
            r=Agenda.query.filter_by(id=int(id)+1,dono_id=current_user.id).first()
            if r: 
                return jsonify(r.toDict())
            else:
                flash("Não há próximo registro consecutivo.")
                return redirect(url_for('agenda.proximo_registro'))
        #r=tratar_tuplas(registro)
    elif request.method=='GET':
            return render_template('retornar_registro.html')
@agenda.route('/pular_letra',methods=['GET','POST'])
@login_required
def proxima_letra():
    if request.method=='POST':
        #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
        letra_atual=Pesquisa.query.filter_by(dono_id=current_user.id).first()
        letra_nova=obter_letra_seguinte(letra_atual.letra)
        if letra_nova==False:
            flash('Erro:Sem valor valido')
            return redirect(url_for('agenda.index'))
        r=Agenda.query.filter(Agenda.nome.ilike(letra_nova.lower()+"%"),Agenda.dono_id==current_user.id)
        if letra_nova in string.ascii_lowercase:
            p=Pesquisa.query.filter_by(dono_id=current_user.id).first()
            search=Pesquisa.query.get(p.id)
            search.letra=letra_nova
            db.session.commit()
        if r:
            return jsonify(handle_agenda(r))
        else:
            flash("Nenhum resultado encontrado")
            return redirect(url_for('agenda.proxima_letra'))
    elif request.method=='GET':
        p=Pesquisa.query.filter_by(dono_id=current_user.id).first()
        return render_template('pular_letra.html',letra=p.letra)
@agenda.route('/apagar_registro',methods=['GET','POST'])
@login_required
def deletar_registro():
    if request.method=='POST':
            #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
            agenda_id=request.form.get("id")
            r=Agenda.query.filter_by(id=agenda_id,dono_id=current_user.id).first()
            db.session.delete(r)
            db.session.commit()
            flash("Item deletado")
            return jsonify(r)
        #r=tratar_tuplas(registro)
    elif request.method=='GET':
            return render_template('apagar_registro.html')
    return redirect(url_for('agenda.index'))
@agenda.route('/atualizar_registro',methods=['GET','POST'])
@login_required
def update_registro():
    if request.method=='POST':
            id=request.form.get('id')
            nome=request.form.get('nome')
            email=request.form.get('email')
            telefone=request.form.get('telefone')
            #__,registro=agenda_db.procurar_por_letra(current_user.id,letra)
            r=Agenda.query.get(id)
            if r:
                if r.dono_id==current_user.id:
                    r.nome=nome
                    r.email=email
                    r.telefone=telefone
                    db.session.commit()
                    return jsonify(r)
                else:
                    flash("Id não acesível para usuário")
                    return redirect(url_for('agenda.update_registro'))
            else:
                flash("Id não equivale a nenhum registro")
                return redirect(url_for('agenda.update_registro'))
        #r=tratar_tuplas(registro)
    elif request.method=='GET':
            return render_template('atualizar_registro.html')
    return r
    
@agenda.route('/criar_registro',methods=['GET','POST'])
@login_required
def adicionar_recursos():
    #json ou formulário
    if request.method=='POST':
        email= request.form.get('email')
        nome=request.form.get('nome')
        telefone= request.form.get('telefone')
        registro=Agenda.query.filter_by(nome=nome,telefone=telefone,dono_id=current_user.id,email=email).first()
        if registro:
            flash('Já existe um registro parecido com este!. Não salvo')
            return redirect(url_for('agenda.index'))
        novo_registro = Agenda(nome=nome,telefone=telefone,email=email,dono_id=current_user.id)
        db.session.add(novo_registro)
        db.session.commit()
        return  redirect(url_for('agenda.index'))
    else:
        return render_template('criar_registro.html')