from django import forms
class FileForm(forms.Form):
    file= forms.FileField(label="file")
    
class IvaNitForm(forms.Form):
   nit = forms.CharField(label="nit")
   fechaIn = forms.CharField(label="fechaIn")
   fechaFin = forms.CharField(label="fechaFIn")
   
class AutorizacionesFechas(forms.Form):
    fechaIn = forms.CharField(label="fechaIn")
    fechaFin = forms.CharField(label="fechaFIn")