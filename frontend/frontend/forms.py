from django import forms
class FileForm(forms.Form):
    file= forms.FileField(label="file")
    
class IvaNitForm(forms.Form):
   nit = forms.CharField(label="nit")
   fechaIn = forms.DateField(label="fechaIn")
   fechaFin = forms.DateField(label="fechaFIn")