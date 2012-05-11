import urllib
import urllib2
from api import *

def getAuth():
    """Realisa a requisicao de identificacao para criar as tabelas"""
    _conn = 'https://www.google.com/accounts/ClientLogin'
    param = urllib.urlencode({'accountType':'GOOGLE','Email':'metanoiaipcg@gmail.com','Passwd':'orareetlabore','service':'fusiontables','source':'TheDataStewards-DataSyncr-1.05'})
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
    token = getAuth()
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

    row = ''
    i = 0
    while i < len(deputados):
        sql = ''
        limit = 500 if 500 <= len(deputados) - i else len(deputados) % 500 
        for j in xrange(limit):
            sql += ";insert into %s (nome, estado, partido) VALUES ('%s', '%s', '%s')" % (table_id, deputados[i+j].nome, deputados[i+j].estado, deputados[i+j].partido)
        
        sql = sql[1:].encode('utf-8')
        query = urllib.urlencode({'sql':sql})
        row += _post(query,token)
        
        i += 500
        
    #print row
    return row
	

token = getAuth()
table_id = create_table_deputados(token)
insert_rows_deputados(token, table_id)


