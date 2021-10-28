from flask import Flask, json,jsonify
from flask_cors import CORS
from xml.etree import ElementTree as ET

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin":"*"}})


@app.route('/')
def index():
    return jsonify({"message":"Api funcionando"})

@app.route('/cargarArchivo',methods=['POST','GET'])
def cargarArchivo():
    return jsonify({"message":"Archivo cargado archivo"})

if __name__=='__main__':
    app.run(debug=True,port=6000)
    