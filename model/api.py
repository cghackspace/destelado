from entities import Assiduidade, Deputado, Gasto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataAPI(object):

    def __init__(self, db_url="sqlite:///test.db"):
        self.__engine__ = create_engine(db_url)
        self.__session__ = sessionmaker(bind = self.__engine__)()
       
    def get_deputados(self):
        return self.__session__.query(Deputado).all()

    def get_deputado_shallow(self, id):
        return self.__session__.query(Deputado).get(id)

    def get_deputado(self, id):
        deputado = self.__session__.query(Deputado).get(id)

        deputado.assiduidades = self.__session__.query(Assiduidade)\
                .filter(Assiduidade.id_deputado == id).all()

        deputado.gastos = self.__session__.query(Gasto)\
                .filter(Gasto.id_deputado == id).all()

        return deputado

if __name__ == '__main__':
    api = DataAPI()

    print api.get_deputados()
    print api.get_deputado(5).assiduidades
    print api.get_deputado(5).gastos
