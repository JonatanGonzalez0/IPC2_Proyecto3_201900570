from re import template
from autorizacion import autorizacion

class procesador:
    def __init__(self) :
        self.lista_Autorizaciones = []
        
    def setLista(self,lista):
        self.lista_Autorizaciones=lista
        
    def getFacturasFecha(self,fecha):
        listaTemp=[]
        
        for aut in self.lista_Autorizaciones:
            aut:autorizacion
            
            if aut.fecha == fecha:
                listaTemp.append(aut)
            
        return listaTemp
    
    def getErroresNitEmisor(self,lista):
        cont =0
        for aut in lista:
            if aut.error =='Nit_Emisor':
                cont+=1
        return cont     
    
    def getErroresNitReceptor(self,lista):
        cont =0
        for aut in lista:
            if aut.error =='Nit_Emisor':
                cont+=1
        return cont  
    
    def getErroresIva(self,lista):
        cont =0
        for aut in lista:
            if aut.error =='Iva':
                cont+=1
        return cont  
    
    def getErroresTotal(self,lista):
        cont =0
        for aut in lista:
            if aut.error =='Total':
                cont+=1
        return cont  
    
    def getErroresReferencia(self,lista):
        cont =0
        for aut in lista:
            if aut.error =='Referencia':
                cont+=1
        return cont  
    
    def ExisteReferencia(self,referencia):
        
        for aut in self.lista_Autorizaciones:
            if aut.referencia == referencia:
                return True
        return False
    
    
    def getCantFacturasCorrectas(self,lista):
        cant = 0
        for aut in lista:
            if aut.error=='OK':
                cant+=1
        return cant
    
    def getAprobaciones(self,lista):
        tempList = []
        for aut in lista:
            if aut.error=='OK':
                tempList.append(aut)
                
        return tempList
    
    def getCantEmisores(self,lista):
        tempList = []
        
        for aut in lista:
            if aut.nitEmisor!='':
                if aut.nitEmisor not in tempList:
                    tempList.append(aut.nitEmisor)

        return len(tempList)
        
    def getCantReceptores(self,lista):
        tempList = []
        
        for aut in lista:
            if aut.nitReceptor!='':
                if aut.nitEmisor not in tempList:
                    tempList.append(aut.nitEmisor)

        return len(tempList)
    
    def deleteFacturasFecha(self,fecha):
        
        for aut in self.lista_Autorizaciones:
            if aut.fecha == fecha:
                self.lista_Autorizaciones.remove(aut)
            

            
           