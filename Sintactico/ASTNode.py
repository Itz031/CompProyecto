class ASTNode:
    def __init__(self, tipo, valor=None):
        self.tipo, self.valor, self.hijos = tipo, valor, []
    def agregar_hijo(self, nodo):
        if nodo: self.hijos.append(nodo)
    def imprimir_arbol(self, prefijo=""):
        val = f" : {self.valor}" if self.valor else ""
        print(f"{prefijo}└── [{self.tipo}]{val}")
        for h in self.hijos: h.imprimir_arbol(prefijo + "    ")