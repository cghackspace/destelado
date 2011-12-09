from flask import Flask
from flask import render_template
from model import api

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/deputados/")
def list_deputados():
    d_api = api.DataAPI()
    deputados = d_api.get_deputados()
    return render_template('deputado/list.html', deputados=deputados)

@app.route("/deputados/<int:dep_id>/")
def get_deputado(dep_id):
    d_api = api.DataAPI()
    deputado = d_api.get_deputado(dep_id)
    if deputado:
      return render_template('deputado/show.html', deputado=deputado)
    else:
      #TODO check if this is correct
      abort(404)

@app.route("/sobre/")
def show_about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run( debug = True )
