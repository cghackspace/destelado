from entities import Assiduidade, Deputado, Gasto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataAPI(object):

    def __init__(self, db_url="sqlite:///test.db"):
        self.__engine__ = create_engine(db_url)
        self.__session__ = sessionmaker(bind = self.__engine__)()

    def __validar_deputado__(self, deputado):
        if not deputado.nome : raise "Nome invalido"
        if not deputado.estado : raise "Nome invalido"
        if not deputado.partido : raise "Nome invalido"
       
    def get_deputados(self):
        return self.__session__.query(Deputado).all()

    def get_deputado_shallow(self, id):
        return self.__session__.query(Deputado).get(id)

    def get_deputado(self, id):
        deputado = self.__session__.query(Deputado).get(id)

        deputado.assiduidades = self.__session__.query(Assiduidade)\
                .filter(Assiduidade.id_deputado == id).all()

        deputado.total_presencas = sum(map(lambda x : x.presencas,\
                deputado.assiduidades))

        deputado.total_faltas = sum(map(lambda x : x.faltas,\
                deputado.assiduidades))

        deputado.gastos = self.__session__.query(Gasto)\
                .filter(Gasto.id_deputado == id).all()

        return deputado

    def inserir_deputado(self, deputado):
        self.__validar_deputado__(deputado)

        self.__session__.add(deputado)
        self.__session__.commit()

        return deputado

    def atualizar_deputado(self, deputado):
        self.__validar_deputado__(deputado)

        self.__session__.merge(deputado)
        self.__session__.commit()

        return deputado

if __name__ == '__main__':
    api = DataAPI()

    print api.get_deputados()
    print api.get_deputado(5).total_presencas
    print api.get_deputado(5).total_faltas
    
