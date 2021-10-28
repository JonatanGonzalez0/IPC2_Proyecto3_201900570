from typing_extensions import TypeVarTuple



class autorizacion:
    def __init__(self,fecha,referencia,EsValida,nitEmisor,nitReceptor,valor,iva,total):
        self.fecha =fecha
        self.referencia = referencia
        self.EsValida = EsValida
        self.nitEmisor =nitEmisor
        self.nitReceptor =nitReceptor
        self.valor = valor
        self.iva = iva
        self.total = total