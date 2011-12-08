from entities import Assiduidade, Deputado, Gasto, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataAPI(object):
    
    CONSULTA_GET_POR_TX_ASSIDUIDADE = """select d.id, (CAST(SUM(a.presencas) as REAL) /
                                                     CAST(SUM(a.presencas + a.faltas)
                                                     as REAL)) as taxa
                                       from deputado d, assiduidade a
                                       where a.id_deputado = d.id
                                       group by d.id order by taxa desc"""

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
       
    def get_deputados(self, order_by_assiduidade = False):
        return self.__session__.query(Deputado).all()

    def get_deputado_shallow(self, id):
        return self.__session__.query(Deputado).get(id)
    
    def get_deputados_por_assiduidade(self):
        '''
        Retorna uma lista com todos os deputados, ordenas por suas taxas de assiduidade,
        onde a taxa de assiduidade eh TOTAL_PRESENCAS / (TOTAL_PRESENCAS + TOTAL_FALTAS).
        Se um deputado nao possui registros de assiduidade, ele nao eh incluso no resultado
        '''
        resultset = self.__engine__.execute(DataAPI.CONSULTA_GET_POR_TX_ASSIDUIDADE)

        deputados = []
        for r in resultset:
            deputado = self.get_deputado_shallow(r[0])
            deputado.taxa_assiduidade = r[1]

            deputados.append(deputado)

        return deputados

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
        self.__session__.merge(assiduidade)
        self.__session__.commit()

        return assiduidade

    def remover_assiduidade(self, assiduidade):
        self.__session__.delete(assiduidade)
        self.__session__.commit()

        return assiduidade

if __name__ == '__main__':
    import datetime

    deputado = Deputado("Fulano", "PB", "???")

    api = DataAPI()

    deputado = api.inserir_deputado(deputado)
    api.inserir_assiduidade(Assiduidade(deputado.id, datetime.date(2011, 1, 1), 1, 10))
    api.inserir_assiduidade(Assiduidade(deputado.id, datetime.date(2011, 1, 1), 2, 11))

    for d in api.get_deputados_por_assiduidade():
        print d.id, d.nome, d.taxa_assiduidade
