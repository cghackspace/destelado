import datetime
import unittest
import api

from entities import Base, Assiduidade, Deputado, Gasto
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class GenericTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        self.api = api.DataAPI()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

class TestDeputado(GenericTest):

    def test_dummy(self):
        # create a configured "Session" class
        Session = sessionmaker(bind=self.engine)

        # create a Session
        session = Session()

        # work with sess
        dep = Deputado('a', 'b', 'c')

        assiduidades = [Assiduidade(0, datetime.date(2011, 1, 1), 10, 20),
                        Assiduidade(0, datetime.date(2011, 2, 1), 10, 25),
                        Assiduidade(0, datetime.date(2011, 3, 1), 10, 30),
                        Assiduidade(0, datetime.date(2011, 4, 1), 10, 35),
                        Assiduidade(0, datetime.date(2011, 5, 1), 10, 40)]
        
        self.api.inserir_deputado(dep)

        for assiduidade in assiduidades:
            assiduidade.id_deputado = dep.id
            self.api.inserir_assiduidade(assiduidade)
        
        
        gastos = [Gasto(0, datetime.date(2011, 1, 1), 'Passeio com a familia', 'Viagem', 1500.45),
                  Gasto(0, datetime.date(2011, 3, 1), 'Caixa 2', 'Roubos', 150220.45),
                  Gasto(0, datetime.date(2011, 5, 1), 'Verba para infra-estrutura', 'Verbas', 300.42)]
        
        for gasto in gastos:
            gasto.id_deputado = dep.id
            self.api.inserir_gasto(gasto)

        print api.DataAPI().get_deputados()
        print api.DataAPI().get_deputado(1)
        print api.DataAPI().get_deputado(1).assiduidades
        print api.DataAPI().get_deputado(1).gastos
        
if __name__ == '__main__':
    unittest.main()
