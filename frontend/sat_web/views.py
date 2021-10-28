import pip._vendor.requests as requests
from django.shortcuts import render
endpoint = 'http://127.0.0.1:5000/'
# Create your views here.

def home(request):
    response = requests.get(endpoint)
    message = response.json()
    context = {
        "message":message
    }
    return render(request,'index.html',context)