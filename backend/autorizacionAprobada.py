
class autorizacionAprobada:
    def __init__(self,fecha,cantFact,cantErrorEmisor,cantErrorReceptor,cantErrorIva,cantErrorReferencia,cantFactCorrectas,cantEmisores,cantReceptores,listaAutorizaciones,cantAprobaciones):
        self.fecha = fecha
        self.facturasRecibidas = cantFact
        self.cantErrorEmisor = cantErrorEmisor
        self.cantErrorReceptor = cantErrorReceptor
        self.cantErrorIva = cantErrorIva
        self.cantErrorReferencia = cantErrorReferencia
        self.FacturasCorrectas = cantFactCorrectas
        self.cantEmisores = cantEmisores
        self.cantReceptores = cantReceptores
        self.listaAutorizaciones = listaAutorizaciones
        self.cantidadAprobaciones = cantAprobaciones
        
        
    