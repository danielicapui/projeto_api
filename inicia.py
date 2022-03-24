from app import db,create_app,Usuario,Agenda
#cria o banco de dados
db.create_all(app=create_app())