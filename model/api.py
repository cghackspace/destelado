from entities import Assiduidade, Deputado, Gasto, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataAPI(object):

    def __init__(self, db_url="sqlite:///test.db"):
        self.__engine__ = create_engine(db_url)
        Base.metadata.create_all(self.__engine__)
        self.__session__ = sessionmaker(bind = self.__engine__)()

    def __validar_deputado__(self, deputado):
        if not deputado.nome : raise "Nome invalido"
        if not deputado.estado : raise "Nome invalido"
        if not deputado.partido : raise "Nome invalido"
    
    def __validar_gasto__(self, gasto):
        if not gasto.id_deputado : raise "Gasto nao associado a um deputado"
        if not gasto.data : raise "Data invalida"
        if not gasto.valor : raise "Valor invalido"
        if not gasto.descricao : raise "Descricao invalido"
        if not gasto.categoria : raise "Categoria invalida"
       

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

    def get_deputado_por_nome(self, nome):
        deputado = self.__session__.query(Deputado)\
                .filter(Deputado.nome == nome).all()
        
        return deputado

    def remover_deputado(self, deputado):
        self.__session__.delete(deputado)
        self.__session__.commit()

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

    def inserir_gasto(self, gasto):
        self.__validar_gasto__(gasto)
        
        self.__session__.add(gasto)
        self.__session__.commit()
        
        return gasto
    
    def remover_gasto(self, gasto):
        self.__session__.delete(gasto)
        
        self.__session__.commit()
    
    def atualizar_gasto(self, gasto):
        self.__validar_gasto__(gasto)
        
        self.__session__.merge(gasto)
        self.__session__.commit()
        
        return gasto

    def inserir_assiduidade(self, assiduidade):
        self.__session__.add(assiduidade)
        self.__session__.commit()

        return assiduidade

    def remover_assiduidade(self, assiduidade):
        self.__session__.delete(assiduidade)
        self.__session__.commit()

        return assiduidade

if __name__ == '__main__':
    print "Nothing to do..."
    
