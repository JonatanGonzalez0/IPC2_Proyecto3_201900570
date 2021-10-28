from autorizacion import autorizacion

class procesador:
    def __init__(self) :
        self.lista_Autorizaciones = []
        
    
        
    def agruparInfo(self,fecha):
        listaTemp=[]
        for aut in self.lista_Autorizaciones:
            aut:autorizacion = aut

            
           