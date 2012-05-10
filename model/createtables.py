import urllib
import urllib2

def getAuth():
    _conn = 'https://www.google.com/accounts/ClientLogin'
    param = urllib.urlencode({'accountType':'GOOGLE','Email':'','Passwd':'','service':'fusiontables','source':'TheDataStewards-DataSyncr-1.05'})
    _return = urllib.urlopen(_conn,param).read()
    nA = _return.find('Auth=')
    _auth = _return[nA+5:len(_return) - 1]
    return _auth


def _post(query,token):
    URL = 'https://www.google.com/fusiontables/api/query'
    headers = {
      'Authorization': 'GoogleLogin auth=' + token,
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    serv_req = urllib2.Request(url=URL,data=query, headers=headers)
    serv_resp = urllib2.urlopen(serv_req)
    return serv_resp.read()

def create_table_deputados(token):
	token = getAuth()
	sql = 'create table Deputados (nome:STRING, estado:STRING, partido:STRING)'
	sql = sql.encode('utf-8')
	query = urllib.urlencode({'sql':sql})
	table = _post(query,token)
	print table
	return table[8:-1]


def insert_row_deputados(token, table_id, nome, estado, partido):
	sql = "insert into %s (nome, estado, partido) VALUES ('%s', '%s', '%s')" % (table_id, nome, estado, partido)
	sql = sql.encode('utf-8')
	query = urllib.urlencode({'sql':sql})
	row = _post(query,token)
	print row
	return row

	

token = getAuth()
table_id = create_table_deputados(token)
insert_row_deputados(token, table_id, 'Uian Sol', 'PB', 'NENHUM')


