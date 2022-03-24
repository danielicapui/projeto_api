import string
def tratar_tuplas(lista):
    d={}
    r={}
    i=0
    print(lista)
    for nome,telefone,email in lista:
        d['nome']=nome
        d['telefone']=telefone
        d['email']=email
        r[i]=d
        i=i+1
    return r
def handle_agenda(registro):   
    from app import Agenda
    r= []
    for i in registro:
        r.append(i.toDict())
    print(r)
    return r

def criar_resposta(status,mensagem,nome_do_conteudo=False,conteudo=False):
    resposta={}
    resposta['status']=status
    resposta['mensagem']=mensagem
    if conteudo and nome_do_conteudo:
        resposta[nome_do_conteudo]=conteudo
    return resposta

def obter_letra_seguinte(atual):
    if atual==None or atual=='z':
        #mensagem:cod:8 e valor:-1
        return False
    p=0
    f=False
    for i in string.ascii_lowercase:
        if f==True:
            p=i
            #mensagem:cod:8 e valor:registro
            print("Proxima letra:".format(p))
            return p
        if atual.lower()==i:
            f=True