
from frontend.forms import FileForm, IvaNitForm
from django.shortcuts import render
import requests


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
            'fechas':'None',
            'Iva_Emisiones':'None',
            'Iva_Recepciones':'None'
        }
    
    if request.method=='POST':
        form = IvaNitForm(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data
            response = requests.post(endpoint + 'ivaNitChart',json = json_data)

    else:
        return render(request,'graficaIvaNit.html',context)   
    
        
        
        
        
        