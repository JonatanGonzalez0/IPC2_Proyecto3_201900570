from flask import Flask,jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin":"*"}})

@app.route('/cargarArchivo',methods=['POST'])
def cargarArchivo():
    return jsonify({"message":"Archivo cargado archivo"})

if __name__=='__main__':
    app.run(debug=True,port=5000)