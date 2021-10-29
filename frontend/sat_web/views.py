from frontend.forms import FileForm
from django.shortcuts import render
import requests
endpoint = 'http://127.0.0.1:5000/'
# Create your views here.

def home(request):
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
            if response.ok:
                context['response'] = "Archivo cargado correctamente"
            else:
                context['response'] = 'No se pudo cargar el archivo'
        else:
            return render(request,'carga.html')
    return render(request,'carga.html',context)