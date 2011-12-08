from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/list/deputados")
def list_deputados():
    pass

if __name__ == "__main__":
    app.run()
