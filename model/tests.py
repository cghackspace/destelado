import datetime
import unittest

from entities import Base, Assiduidade, Deputado
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class TestDeputado(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_dummy(self):
        # create a configured "Session" class
        Session = sessionmaker(bind=self.engine)

        # create a Session
        session = Session()

        # work with sess
        dep = Deputado('a', 'b', 'c')

        assiduidade = Assiduidade(0, datetime.date(2011, 1, 1), 10, 20)

        session.add(dep)
        session.commit()

        assiduidade.id_deputado = dep.id
        session.add(assiduidade)
        session.commit()

        print session.query(Deputado).all()
        print session.query(Assiduidade).all()

if __name__ == '__main__':
    unittest.main()
