from flask import Flask
from flask import render_template
from model import fakeapi

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/deputados")
def list_deputados():
    deputados = fakeapi.get_deputados()
    return render_template('deputado/list.html', deputados=deputados)

@app.route("/deputados/<int:dep_id>")
def get_deputado(dep_id):
    deputado = fakeapi.get_deputado(dep_id)
    if deputado:
      return render_template('deputado/show.html', deputado=deputado)
    else:
      #TODO check if this is correct
      abort(404)

if __name__ == "__main__":
    app.run( debug = True )
