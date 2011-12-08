from model.entities import *

def get_deputados():
    deputados = []
    d = Deputado(nome='Teste 1', estado='PB', partido='PT')
    d.id = 1
    deputados.append( d )

    d = Deputado(nome='Teste 2', estado='PB', partido='PMDB')
    d.id = 2
    deputados.append( d )

    d = Deputado(nome='Teste 3', estado='PB', partido='PSOL')
    d.id = 3
    deputados.append( d )
    return deputados

def get_deputado(dep_id):
    deputados = get_deputados()
    for d in deputados:
        if d.id == dep_id:
            return d

    return None

