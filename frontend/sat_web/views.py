
from frontend.forms import FileForm, IvaNitForm, AutorizacionesFechas
from django.shortcuts import render
from django.http import FileResponse
import requests

from frontend.settings import PDF_FILES_FOLDER


endpoint = 'http://127.0.0.1:5000/'
# Create your views here.

def home(request):
    response = requests.get(endpoint)
    return render(request,'index.html')

def cargaMasiva(request):
    context = {
        'content':'Esperando Datos',
        'response':'No hay Respuesta'
    }
    
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_bin = f.read()
            xml = xml_bin.decode('utf-8')
            context['content']= xml
            
            
            response = requests.post(endpoint+'cargarArchivo',data = xml_bin)
            response_data = response.json()
            if response.ok:
                context['response'] = response_data['dataProcesada']
            else:
                context['response'] = 'No se pudo cargar el archivo'
        else:
            return render(request,'carga.html')
    return render(request,'carga.html',context)

def baseDatos(request):
    context = {
        'estadoBase':'None',
        'BaseDatos':'None'
    }
    
    if request.method == 'POST':
        
        response = requests.post(endpoint+'baseDatos')
        
        response_data = response.json()
        
        if response.ok:
            context['estadoBase']= response_data['estadoBase']
            context['BaseDatos'] = response_data['BaseDatos']
        else:
            context['estadoBase']='No se pudo eliminar la Base de Datos'
    else:
        response = requests.get(endpoint+'baseDatos')
        response_data = response.json()
        
        if response.ok:
            context['estadoBase']= response_data['estadoBase']
            context['BaseDatos'] = response_data['BaseDatos']
        else:
            context['estadoBase']='No se pudo oibtener la Base de Datos'
    
    return render(request,'VistaBase.html',context)

def ivaNit(request):
    context={
            'fechasNitEmision':'None',
            'ValoresIvaEmitido':'None',
            'fechasNitReceptor':'None',
            'valoresIvaRecibido':'None'
        }
    
    if request.method=='POST':
        form = IvaNitForm(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data
            
            response = requests.post(endpoint + 'ivaNitChart',json = json_data)
            
            response_data = response.json()
            if response_data:
                
                context['fechasNitEmision'] = response_data['fechasNitEmision']
                context['ValoresIvaEmitido'] = response_data['ValoresIvaEmitido']
                context['fechasNitReceptor'] = response_data['fechasNitReceptor']
                context['valoresIvaRecibido'] = response_data['valoresIvaRecibido']

                return render(request,'graficaIvaNit.html',context)
            else:
                return render(request,'graficaIvaNit.html')  
        else:
            return render(request,'graficaIvaNit.html',{'form':form})      
    else:
        return render(request,'graficaIvaNit.html')   
    
        
def autoValorTotal(request):
    context={
            'fechas_Autorizacion':'None',
            'totales_Sin_Iva':'None',
            'totales_Con_Iva':'None',
        }
    
    if request.method=='POST':
        form = AutorizacionesFechas(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data
            
            response = requests.post(endpoint + 'autValorTotal',json = json_data)
            
            response_data = response.json()
            if response_data:
                context['fechas_Autorizacion'] = response_data['fechas_Autorizacion']
                context['totales_Sin_Iva'] = response_data['totales_Sin_Iva']
                context['totales_Con_Iva'] = response_data['totales_Con_Iva']
        
                return render(request,'graficaValorTotal.html',context)   
            else:
                return render(request,'graficaValorTotal.html')  
        else:
            return render(request,'graficaValorTotal.html',{'form':form})      
    else:
        return render(request,'graficaValorTotal.html')     
        
def ayuda(request):
    return render(request,'ayuda.html')

def pdfDocumentacion(request):
    pdfDoc = open(PDF_FILES_FOLDER + '\Documentacion.pdf','rb')
    return FileResponse(pdfDoc)