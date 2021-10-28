
import re
from flask import Flask, json,jsonify,request
from flask_cors import CORS
from xml.etree import ElementTree as ET

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin":"*"}})

Listado_Autorizaciones = []

contadorAutorizaciones = 0
@app.route('/',methods=['GET'])
def index():
    if request.method=='GET':
        return jsonify({"message":"Api funcionando"})

@app.route('/cargarArchivo',methods=['POST'])
def cargarArchivo():
    xml = request.data.decode('utf-8')
    root = ET.XML(xml)
    
    datosDTE = root.findall('DTE')
    for solicitud in datosDTE:
        
        fecha  = solicitud.find('TIEMPO').text
        matchFecha = re.search(r'\d{2}/\d{2}/\d{4}',fecha).group()
        
        referencia = solicitud.find('REFERENCIA').text
        
        Nit_Emisor = solicitud.find('NIT_EMISOR').text
        Nit_Emisor_Correcto = verificarNit(Nit_Emisor)
        
        Nit_Receptor = solicitud.find('NIT_RECEPTOR').text
        Nit_Receptor_Correcto = verificarNit(Nit_Receptor)
        
        valor = solicitud.find('VALOR').text
        
        iva = solicitud.find('IVA').text
        iva_Correcto = verificarIva(valor,iva)
        
        total = solicitud.find('TOTAL').text
        total_Correcto = verificarTotal(valor,total)
        
        
        
    
    return jsonify({"message":"Archivo cargado archivo"})

def verificarNit(nit):
    longitud =len(nit)
    
    acumSuma = 0
    contRevers = 2
    for i in range(longitud-2,-1,-1):
        multiplicacion = int(nit[i])*contRevers
        contRevers+=1
        
        acumSuma +=multiplicacion

    modul = acumSuma%11
    
    rest = 11- modul 
    
    resutl = rest%11
    print(str(resutl))
    
    if resutl<10 and resutl== int(nit[longitud-1]):
        return True
    else:
        return False
        
def verificarIva(valor,iva):
    valor = float(valor)  
    
    iva = float(iva)
    
    ivaComprobador = round( float(valor*0.12),2)
    
    if ivaComprobador==iva:
        return True
    else:
        return False
    
def verificarTotal(valor,total):
    valor = float(valor)
    iva = float(valor*0.12) 
    
    totalCorrecto = round(valor+iva,2) 
    
    total = round(float(total),2) 
    
    if totalCorrecto == total:
        return True
    else:
        return False

if __name__=='__main__':
    app.run(debug=True,port=5000)
    