
import os
import re
from xml.etree import ElementTree as ET
import datetime
from operator import attrgetter
from flask import Flask, jsonify, request
from flask_cors import CORS

from aprobacion import aprobacion
from autorizacion import autorizacion
from autorizacionAprobada import autorizacionAprobada
from procesadorInfo import procesador

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin":"*"}})

BaseDatos = []

@app.route('/',methods=['GET'])
def index():
    if request.method=='GET':
        UpdateBase()
        return jsonify({"message":"Api funcionando Base Cargada"})

@app.route('/cargarArchivo',methods=['POST'])
def cargarArchivo():
    global BaseDatos
    xml = request.data.decode('utf-8')
    root = ET.XML(xml)
    
    datosDTE = root.findall('DTE')
    
    proceso = procesador()
    
    for solicitud in datosDTE:
        fecha  = solicitud.find('TIEMPO').text
        matchFecha = re.search(r'\d{2}/\d{2}/\d{4}',fecha).group()
        
        referencia = solicitud.find('REFERENCIA').text
        
        if proceso.ExisteReferencia(referencia)==True:
            proceso.lista_Autorizaciones.append(autorizacion(matchFecha,"","","","'","''","''",error='Referencia'))
            continue
        Nit_Emisor = solicitud.find('NIT_EMISOR').text
        Nit_Emisor_Correcto = verificarNit(Nit_Emisor)
        
        
        if Nit_Emisor_Correcto== False:
            proceso.lista_Autorizaciones.append(autorizacion(matchFecha,"","","","'","''","''",error='Nit_Emisor'))
            continue
            
        Nit_Receptor = solicitud.find('NIT_RECEPTOR').text
        Nit_Receptor_Correcto = verificarNit(Nit_Receptor)
        
        if Nit_Receptor_Correcto== False:
            proceso.lista_Autorizaciones.append(autorizacion(matchFecha,"","","","'","''","''",error='Nit_Receptor'))
            continue
        
        valor = solicitud.find('VALOR').text
        
        iva = solicitud.find('IVA').text
        iva_Correcto = verificarIva(valor,iva)
        
        if iva_Correcto == False:
            proceso.lista_Autorizaciones.append(autorizacion(matchFecha,"","","","'","''","''",error='Iva'))
            continue
        
        total = solicitud.find('TOTAL').text
        total_Correcto = verificarTotal(valor,total)
        
        if total_Correcto == False:
            proceso.lista_Autorizaciones.append(autorizacion(matchFecha,"","","","'","''","''",error='Total'))
            continue
        
        #SI paso todos los verificadores, el dte esta correcto y se almacena
        proceso.lista_Autorizaciones.append(autorizacion(matchFecha,referencia,Nit_Emisor,Nit_Receptor,valor,iva,total,error='OK'))
    
    Carpeta_Raiz = os.path.dirname(os.path.abspath(__file__))
    tree = ET.parse(Carpeta_Raiz+'/Base_Autorizaciones.xml')
    
    root = tree.getroot()
    
    while(len(proceso.lista_Autorizaciones)>0):

        autorizacionChild = ET.SubElement(root,'AUTORIZACION')
        
        fecha = proceso.lista_Autorizaciones[0].fecha
        
        #Hijo de Fecha 
        fechaChild = ET.SubElement(autorizacionChild,'FECHA')
        fechaChild.text= fecha
        
        datosFacturas = proceso.getFacturasFecha(fecha)
        
        #hijo facturas Recibidas
        facturasRecibidas = ET.SubElement(autorizacionChild,'FACTURAS_RECIBIDAS')
        canFacturasRecibidas = len(datosFacturas)
        facturasRecibidas.text = str(canFacturasRecibidas)
        
        #hijo de Errores en la autorizacion 
        erroresChild = ET.SubElement(autorizacionChild,'ERRORES')
        
        contNitEmisor = proceso.getErroresNitEmisor(datosFacturas)
        NitEmisorError =  ET.SubElement(erroresChild,'NIT_EMISOR')
        NitEmisorError.text = str(contNitEmisor)
        
        contNitReceptor = proceso.getErroresNitReceptor(datosFacturas)
        catNitReceptorError =  ET.SubElement(erroresChild,'NIT_RECEPTOR')
        catNitReceptorError.text = str(contNitReceptor)
        
        contErrorIva = proceso.getErroresIva(datosFacturas)
        ErrorIva =  ET.SubElement(erroresChild,'IVA')
        ErrorIva.text = str(contErrorIva)
        
        contErrorReferencia = proceso.getErroresReferencia(datosFacturas)
        ErrorReferencia =  ET.SubElement(erroresChild,'REFERENCIA_DUPLICADA')
        ErrorReferencia.text = str(contErrorReferencia)
        
        #hijo CantAprobaciones
        cantAprobaciones = ET.SubElement(autorizacionChild,'FACTURAS_CORRECTAS')
        conteoAprob = proceso.getCantFacturasCorrectas(datosFacturas)
        cantAprobaciones.text = str(conteoAprob)
        
        
        #hijo CantEmisores
        cantEmisores = ET.SubElement(autorizacionChild,'CANTIDAD_EMISORES')
        cantEmi = proceso.getCantEmisores(datosFacturas)
        cantEmisores.text = str(cantEmi)
        
        #hijo CantReceptores
        cantEmisores = ET.SubElement(autorizacionChild,'CANTIDAD_RECEPTORES')
        cantRecep = proceso.getCantReceptores(datosFacturas)
        cantEmisores.text = str(cantRecep)
        
        
        #hijo de Errores en la autorizacion 
        listado_Autorizaciones = ET.SubElement(autorizacionChild,'LISTADO_AUTORIZACIONES')
        
        Aprobaciones = proceso.getAprobaciones(datosFacturas)
        
        cod = 0
        
        for aprobacion in Aprobaciones:
            aprobacion:autorizacion
            cod +=1
            codigo = str(cod)
            codFil = codigo.zfill(8)
            Fech = fecha.split('/')
            
            dia = Fech[0]
            mes = Fech[1]
            anio = Fech[2]
            StrFech = anio+mes+dia
            codigoFormat = StrFech + codFil
            
            aprobacionChild = ET.SubElement(listado_Autorizaciones,'APROBACION')
            
            NitEmisorChild = ET.SubElement(aprobacionChild,'NIT_EMISOR',)
            NitEmisorChild.text = aprobacion.nitEmisor
            NitEmisorChild.set('ref', aprobacion.referencia)
            
            codAprobacionChild = ET.SubElement(aprobacionChild,'CODIGO_APROBACION')
            codAprobacionChild.text = codigoFormat
            
            NitReceptorChild = ET.SubElement(aprobacionChild,'NIT_RECEPTOR',)
            NitReceptorChild.text = aprobacion.nitReceptor
            
            ValorChild = ET.SubElement(aprobacionChild,'VALOR',)
            ValorChild.text = aprobacion.valor
            
        catAprobacionesChil = ET.SubElement(listado_Autorizaciones,'CANTIDAD_APROBACIONES')
        conteoAprob = proceso.getCantFacturasCorrectas(datosFacturas)
        catAprobacionesChil.text = str(conteoAprob)
            
        
        proceso.deleteFacturasFecha(fecha)
    
    
    ET.indent(tree, space="\t", level=0) 
    rutaBase =Carpeta_Raiz+'/Base_Autorizaciones.xml'  
    tree.write(rutaBase,encoding='utf-8')
   
    
    xmlResult = ET.tostring(root, encoding='utf8').decode('utf8')
    return jsonify({"dataProcesada":xmlResult})
    
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

def UpdateBase():
    Carpeta_Raiz = os.path.dirname(os.path.abspath(__file__))
    tree = ET.parse(Carpeta_Raiz+'/Base_Autorizaciones.xml')
    
    root = tree.getroot()
    
    autorizaciones = root.findall('AUTORIZACION')
    global BaseDatos
    if autorizaciones:
        
        for aut in autorizaciones:
            fecha = aut.find('FECHA').text
            
            cantFacturas = int(aut.find('FACTURAS_RECIBIDAS').text)
            
            error = aut.find('ERRORES')
            
            ErrEmisor = error.find('NIT_EMISOR')
            ErrReceptor = error.find('NIT_RECEPTOR')
            ErrIVA = error.find('IVA')
            ErrRef = error.find('REFERENCIA_DUPLICADA')
            
            cantFactCorrectas = int(aut.find('FACTURAS_CORRECTAS').text) 
            cantEmisor = int(aut.find('CANTIDAD_EMISORES').text)
            cantReceptor = int(aut.find('CANTIDAD_RECEPTORES').text)
            
            listaAutorizaciones = aut.find('LISTADO_AUTORIZACIONES')
        
            aprobaciones = listaAutorizaciones.findall('APROBACION')
            listaAut = []
            
            if len(aprobaciones)>0:
                for aprob in aprobaciones:
                    childNitemisor = aprob.find('NIT_EMISOR')
                    nitEmisor = childNitemisor.text
                    strRef = childNitemisor.get('ref')

                    codAprobacion = aprob.find('CODIGO_APROBACION').text
                    
                    nitReceptor = aprob.find('NIT_RECEPTOR').text
                    valor = round(float(aprob.find('VALOR').text),2)
                    
                    listaAut.append(aprobacion(nitEmisor,strRef,codAprobacion,nitReceptor,valor))

                cantAprobaciones = len(listaAut)
                
                BaseDatos.append(autorizacionAprobada(fecha,cantFacturas,ErrEmisor,ErrReceptor,ErrIVA,ErrRef,cantFactCorrectas,cantEmisor,cantReceptor,listaAut,cantAprobaciones))
            else:
                BaseDatos.append(autorizacionAprobada(fecha,cantFacturas,ErrEmisor,ErrReceptor,ErrIVA,ErrRef,cantFactCorrectas,cantEmisor,cantReceptor,None,0))
                
    else:
        BaseDatos=None
              
@app.route('/baseDatos',methods=['POST','GET'])     
def baseDatos():
    if request.method=='POST':
        #si es post, el usuario activo el boton eliminar
        xml_data = "<LISTAAUTORIZACIONES></LISTAAUTORIZACIONES>"
        print(ET.canonicalize(xml_data))
        
        Carpeta_Raiz = os.path.dirname(os.path.abspath(__file__))
        rutaBase =Carpeta_Raiz+'/Base_Autorizaciones.xml'  
        
        with open(rutaBase, mode='w', encoding='utf-8') as out_file:
            ET.canonicalize(xml_data, out=out_file)

        tree = ET.parse(rutaBase)
        root = tree.getroot()   
        
        xmlResult = ET.tostring(root, encoding='utf8').decode('utf8')
        
        return jsonify({"estadoBase":"Base Eliminada","BaseDatos":xmlResult})   
    
    elif request.method=='GET':
        Carpeta_Raiz = os.path.dirname(os.path.abspath(__file__))
        rutaBase =Carpeta_Raiz+'/Base_Autorizaciones.xml'
        tree = ET.parse(rutaBase)
        root = tree.getroot()   
        
        xmlResult = ET.tostring(root, encoding='utf8').decode('utf8')
        
        return jsonify({"estadoBase":"Base Actualizada","BaseDatos":xmlResult})

UpdateBase()

@app.route('/ivaNitChart',methods=['POST','GET'])

def ivaNit():
    global BaseDatos
    baseDatos.sort(key = lambda r: r.fecha)
    
    if request.method == 'GET':
        
       
        
       
        


        
    

if __name__=='__main__':
    app.run(debug=True,port=5000)
    