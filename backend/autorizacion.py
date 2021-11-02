class autorizacion:
    def __init__(self,fecha,referencia,nitEmisor,nitReceptor,valor,iva,total,error):
        self.fecha =fecha
        self.referencia = referencia
        self.nitEmisor =nitEmisor
        self.nitReceptor =nitReceptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.error= error