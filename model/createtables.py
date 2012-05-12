import urllib
import urllib2
from api import *
import time

def getAuth():
    """Realisa a requisicao de identificacao para criar as tabelas"""
    _conn = 'https://www.google.com/accounts/ClientLogin'
    param = urllib.urlencode({'accountType':'GOOGLE','Email':'','Passwd':'','service':'fusiontables','source':'TheDataStewards-DataSyncr-1.05'})
    _return = urllib.urlopen(_conn,param).read()
    nA = _return.find('Auth=')
    _auth = _return[nA + 5 : len(_return) - 1]
    return _auth


def _post(query,token):
    """Faz um REQUEST POST para os servidores do google fusion table"""
    URL = 'https://www.google.com/fusiontables/api/query'
    headers = {
      'Authorization': 'GoogleLogin auth=' + token,
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    serv_req = urllib2.Request(url=URL,data=query, headers=headers)
    serv_resp = urllib2.urlopen(serv_req)
    return serv_resp.read()


def create_table_deputados(token):
    """Cria a tabela Deputados (colunas -> nome|estado|partido)"""
    sql = 'create table Deputados (nome:STRING, estado:STRING, partido:STRING)'
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    table = _post(query,token)
    #print table
    return table[8:-1]


def insert_row_deputados(token, table_id, nome, estado, partido):
    """Insere uma unica linhas na tabela Deputados, fornecendo dados"""
    sql = "insert into %s (nome, estado, partido) VALUES ('%s', '%s', '%s')" % (table_id, nome, estado, partido)
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    row = _post(query,token)
    #print row
    return row


def insert_rows_deputados(token, table_id):
    """Insere todas as linhas na tabela Deputados, pegando do db local"""
    data = DataAPI()
    deputados = data.get_deputados()

    rows = ''
    i = 0
    while i < len(deputados):
        sql = ''
        limit = 500 if 500 <= len(deputados) - i else len(deputados) % 500 
        for j in xrange(limit):
            sql += ";insert into %s (nome, estado, partido) VALUES ('%s', '%s', '%s')" % (table_id, deputados[i+j].nome, deputados[i+j].estado, deputados[i+j].partido)
        
        sql = sql[1:].encode('utf-8')
        query = urllib.urlencode({'sql':sql})
        rows += _post(query, token)
        
        i += 500
        
    #print rows
    return rows
	

def create_table_gastos(token):
    """Cria a tabela Gastos (colunas -> id_deputado|ano|descricao|categoria|valor)"""
    sql = 'create table Gastos (id_deputado:NUMBER, ano:NUMBER, descricao:STRING, categoria:STRING, valor:NUMBER)'
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    table = _post(query, token)
    print table
    return table[8:-1]


def insert_row_gastos(token, table_id, id_deputado, ano, descricao, categoria, valor):
    """Insere uma unica linhas na tabela Gastos, fornecendo dados"""
    sql = "insert into %s (id_deputado, ano, descricao, categoria, valor) VALUES (%d, %d, '%s', '%s', %d)" % (table_id, id_deputado, ano, descricao, categoria, valor)
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    row = _post(query, token)
    #print row
    return row    


def insert_rows_gastos(token, table_id):
    """Insere todas as linhas na tabela Gastos, pegando do db local"""
    data = DataAPI()
    deputados = data.get_deputados()

    rows = ''
    i = 0
    while i < len(deputados):
        sql = ''
        count = 0
        j = 0
        while i + j < len(deputados):
            if len(deputados[i+j].gastos) == 0:
                j += 1
                pass
            if count + len(deputados[i+j].gastos) >= 500: break
           
            for k in xrange(len(deputados[i+j].gastos)):
                id_deputado = int(deputados[i+j].gastos[k].id_deputado)
                ano = int(deputados[i+j].gastos[k].ano)
                descricao = deputados[i+j].gastos[k].descricao
                categoria = deputados[i+j].gastos[k].categoria
                valor = float(deputados[i+j].gastos[k].valor)
              
                sql += ";insert into %s (id_deputado, ano, descricao, categoria, valor) VALUES (%d, %d, '%s', '%s', %d)" % (table_id, id_deputado, ano, descricao, categoria, valor)
                
            count += len(deputados[i+j].gastos)
            j += 1
        i += j

        sql = sql[1:].encode('utf-8')
        query = urllib.urlencode({'sql':sql})
        rows += _post(query, token)
        time.sleep(0.1)

    #print rows
    return rows           


def create_table_assiduidade(token):
    """Cria a tabela Assiduidade (colunas -> id_deputado|data|presencas|faltas)"""
    sql = 'create table Assiduidade (id_deputado:NUMBER, data:DATETIME, presencas:NUMBER, faltas:NUMBER)'
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    table = _post(query, token)
    print table
    return table[8:-1]


def insert_row_assiduidade(token, table_id, id_deputado, data, presencas, faltas):
    """Insere uma unica linhas na tabela Assiduidade, fornecendo dados"""
    sql = "insert into %s (id_deputado, data, presencas, faltas) VALUES (%d, '%s', %d, %d)" % (table_id, id_deputado, data, presencas, faltas)
    sql = sql.encode('utf-8')
    query = urllib.urlencode({'sql':sql})
    row = _post(query, token)
    #print row
    return row    


def insert_rows_assiduidade(token, table_id):
    """Insere todas as linhas na tabela Assiduidade, pegando do db local"""
    data = DataAPI()
    deputados = data.get_deputados()

    rows = ''
    i = 0
    while i < len(deputados):
        sql = ''
        count = 0
        j = 0
        while i + j < len(deputados):
            if len(deputados[i+j].assiduidades) == 0:
                j += 1
                pass
            if count + len(deputados[i+j].assiduidades) >= 500: break
           
            for k in xrange(len(deputados[i+j].assiduidades)):
                id_deputado = int(deputados[i+j].assiduidades[k].id_deputado)
                ano = int(deputados[i+j].assiduidades[k].data.year)
                mes = deputados[i+j].assiduidades[k].data.month
                dia = deputados[i+j].assiduidades[k].data.day
                presencas = int(deputados[i+j].assiduidades[k].presencas)
                faltas = int(deputados[i+j].assiduidades[k].faltas) 
              
                sql += ";insert into %s (id_deputado, data, presencas, faltas) VALUES (%d, '%d.%d.%d', %d, %d)" % (table_id, id_deputado, ano, mes, dia, presencas, faltas)
                
            count += len(deputados[i+j].assiduidades)
            j += 1
        i += j

        sql = sql[1:].encode('utf-8')
        query = urllib.urlencode({'sql':sql})
        rows += _post(query, token)
        time.sleep(0.1)

    #print rows
    return rows           



### START UPLOAD ###
#token = getAuth()
#table_id = create_table_deputados(token)
#ids_deputados = insert_rows_deputados(token, table_id)

#table_id = create_table_gastos(token)
#rows = insert_rows_gastos(token, table_id)

#table_id = create_table_assiduidade(token)
#rows = insert_rows_assiduidade(token, table_id)
#print rows
