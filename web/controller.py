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
    print deputados

@app.route("/deputados/<id>")
def get_deputado(dep_id):
    pass

if __name__ == "__main__":
    app.run( debug = True )
