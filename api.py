import os
import re
from flask import Flask, jsonify,request
from flask_cors import CORS
from xml.etree import ElementTree as ET
from autorizacion import autorizacion

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin":"*"}})



@app.route('/',methods=['GET'])
def index():
    if request.method=='GET':
        return jsonify({"message":"Api funcionando"})

@app.route('/cargarArchivo',methods=['POST'])
def cargarArchivo():
    xml = request.data.decode('utf-8')
    root = ET.XML(xml)
    
    datosDTE = root.findall('DTE')
    
    Listado_Autorizaciones = []
    contadorErrorNitEmisor = 0
    contadorErrorNitReceptor = 0
    contadorErrorIva = 0
    contadorErrorTotal = 0 
    contadorFacturas = 0
    contadorFacturasSinError=0
    contadorFacturasError = 0
    
    for solicitud in datosDTE:
        fecha  = solicitud.find('TIEMPO').text
        matchFecha = re.search(r'\d{2}/\d{2}/\d{4}',fecha).group()
        
        referencia = solicitud.find('REFERENCIA').text
        
        Nit_Emisor = solicitud.find('NIT_EMISOR').text
        Nit_Emisor_Correcto = verificarNit(Nit_Emisor)
        
        
        if Nit_Emisor_Correcto== False:
            contadorErrorNitEmisor+=1
            contadorFacturasError+=1
            contadorFacturas+=1
            continue
            
        Nit_Receptor = solicitud.find('NIT_RECEPTOR').text
        Nit_Receptor_Correcto = verificarNit(Nit_Receptor)
        
        if Nit_Receptor_Correcto== False:
            contadorErrorNitReceptor+=1
            contadorFacturasError+=1
            contadorFacturas+=1
            continue
        
        valor = solicitud.find('VALOR').text
        
        iva = solicitud.find('IVA').text
        iva_Correcto = verificarIva(valor,iva)
        
        if iva_Correcto == False:
            contadorErrorIva+=1
            contadorFacturasError+=1
            contadorFacturas+=1
            continue
        
        total = solicitud.find('TOTAL').text
        total_Correcto = verificarTotal(valor,total)
        
        if total_Correcto == False:
            contadorErrorTotal +=1
            contadorFacturasError+=1
            contadorFacturas+=1
            continue
        
        
        #SI paso todos los verificadores, el dte esta correcto y se almacena
        Listado_Autorizaciones.append(autorizacion(matchFecha,referencia,Nit_Emisor,Nit_Receptor,valor,iva,total,error=None))
        contadorFacturas+=1
        contadorFacturasSinError +=1
     
    Carpeta_Raiz = os.path.dirname(os.path.abspath(__file__))
    tree = ET.parse(Carpeta_Raiz+'/Base_Autorizaciones.xml')
    
    root = tree.getroot()
       
    autorizacionesTree = root.findall('AUTORIZACION')
    cod = ''
    if len(autorizacionesTree)>0:
        
        for aut in autorizacionesTree:
            cod = aut.find('CODIGO_APROBACION').text
    else:
        cod = 1
    
    autorizacionChild = ET.SubElement(root,'AUTORIZACION')
    
    if cod ==1:
        codigo = '1'
        str2 = codigo.zfill(10)
    
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