from django.shortcuts import render
endoponint = 'http://127.0.0.1:6000/'
# Create your views here.

def home():
    return render('index.html')