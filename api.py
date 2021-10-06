from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')

def index():
    return'Pagina Principal Index'

@app.route('/cargarArchivo',methods=['POST'])
def cargarArchivo():
    return jsonify({"message":"Archivo cargado archivo"})

if __name__=='__main__':
    app.run(debug=True,port=5000)