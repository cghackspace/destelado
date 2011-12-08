from model.entities import *

def get_deputados():
    deputados = []
    deputados.append( Deputado(id=1, nome='Teste 1', estado='PB', partido='PT') )
    return deputados
