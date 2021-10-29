
class aprobacion:
    def __init__(self,nitEmisor,referencia,codAprobacion,nitReceptor,valor,):
        self.Nit_Emisor = nitEmisor
        self.referencia = referencia
        self.Cod_Aprobacion = codAprobacion
        self.Nit_Receptor = nitReceptor
        self.valor = float(valor)
        self.iva = round(float(valor*0.12),2)
        self.total = round(self.valor + self.iva,2)