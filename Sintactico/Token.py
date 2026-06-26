class Token:
    def __init__(self, tipo, valor, linea=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea 

    def __str__(self):
        return f"[{self.tipo.name}: {self.valor}]"
