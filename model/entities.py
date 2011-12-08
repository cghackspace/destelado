import datetime

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Deputado(Base):
    __tablename__ = 'deputado'

    id = Column(Integer, primary_key = True)
    nome = Column(String)
    estado = Column(String)
    partido = Column(String)

    def __init__(self, nome, estado, partido):
        self.nome = nome
        self.estado = estado
        self.partido = partido

    def __repr__(self):
        return "Deputado %d:%s" % (self.id, self.nome)

class Assiduidade(Base):
    __tablename__ = 'assiduidade'

    id_deputado = Column(Integer, ForeignKey('deputado.id'), primary_key = True)
    data = Column(Date, primary_key=True)
    presencas = Column(Integer)
    faltas = Column(Integer)

    def __init__(self, id_deputado, data, presencas, faltas):
        self.id_deputado = id_deputado
        self.data = data
        self.presencas = presencas
        self.faltas = faltas

    def __repr__(self):
        return "Em %s, o deputado %d faltou %d vezes e compareceu %d vezes" % (self.data, self.id_deputado, self.faltas, self.presencas)

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    id_deputado = Column(Integer, ForeignKey('deputado.id'))
    data = Column(Date)
    descricao = Column(String)
    categoria = Column(String)
    valor = Column(Numeric)

    def __init__(self, id_deputado, data, descricao, categoria, valor):
        self.id_deputado = id_deputado
        self.data = data
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor

    def __repr__(self):
        return 'Na categoria %s o deputado %d gastou R$%.2f em %s' % (self.categoria, self.id_deputado, self.valor, self.data)

if __name__ == '__main__':
    some_engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(some_engine) 

    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()

    # work with sess
    dep = Deputado('a', 'b', 'c')

    assiduidade = Assiduidade(0, datetime.date(2011, 1, 1), 10, 20)

    gasto = Gasto(0, datetime.date(2011, 1, 1), 'Passeio com a familia', 'Viagem', 1500.45)

    session.add(dep)
    session.commit()

    assiduidade.id_deputado = dep.id
    session.add(assiduidade)
    session.commit()

    gasto.id_deputado = dep.id
    session.add(gasto)
    session.commit()

    print session.query(Deputado).all()
    print session.query(Assiduidade).all()
    print session.query(Gasto).all()
