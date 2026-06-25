from Sintactico.Catalogo import TokenType
from ASTNode import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0
        
    def actual(self): return self.tokens[self.pos]
    
    def coincidir(self, tipo):
        if self.actual().tipo == tipo:
            t = self.actual()
            self.pos += 1
            return t
        return None
        
    def esperar(self, tipo):
        t = self.coincidir(tipo)
        if not t: 
            # ¡AQUÍ GENERAMOS EL ERROR DE SINTAXIS AMIGABLE!
            actual = self.actual()
            raise SyntaxError(f"Error de Sintaxis en la línea {actual.linea}: Se esperaba '{tipo.name}' pero se encontro '{actual.valor}'")
        return t
        
    def parse(self):
        root = ASTNode("PROGRAMA")
        while self.actual().tipo != TokenType.EOF: 
            root.agregar_hijo(self.parse_funcion()) # Ahora exige leer funciones (int main)
        return root
        
    def parse_funcion(self):
        self.esperar(TokenType.INT)
        nombre = self.esperar(TokenType.IDENTIFICADOR)
        self.esperar(TokenType.PARENTESIS_IZQ)
        self.esperar(TokenType.PARENTESIS_DER)
        self.esperar(TokenType.LLAVE_IZQ)
        
        n = ASTNode("FUNCION", nombre.valor)
        b = ASTNode("BLOQUE")
        while self.actual().tipo != TokenType.LLAVE_DER and self.actual().tipo != TokenType.EOF: 
            b.agregar_hijo(self.parse_sentencia())
            
        self.esperar(TokenType.LLAVE_DER)
        n.agregar_hijo(b)
        return n
        
    def parse_sentencia(self):
        t = self.actual().tipo
        if t == TokenType.INT: return self.parse_declaracion()
        elif t == TokenType.IDENTIFICADOR: return self.parse_asignacion()
        elif t == TokenType.PRINT: return self.parse_impresion()
        elif t == TokenType.WHILE: return self.parse_while()
        elif t == TokenType.IF: return self.parse_if()
        elif t == TokenType.RETURN: return self.parse_return()
        else: 
            actual = self.actual()
            raise SyntaxError(f"Error de Sintaxis en la línea {actual.linea}: Instrucción no reconocida '{actual.valor}'")
            
    def parse_declaracion(self):
        self.esperar(TokenType.INT)
        n = ASTNode("DECLARACION", self.esperar(TokenType.IDENTIFICADOR).valor)
        if self.coincidir(TokenType.ASIGNACION): n.agregar_hijo(self.parse_expresion())
        self.esperar(TokenType.PUNTO_COMA)
        return n
        
    def parse_asignacion(self):
        n = ASTNode("ASIGNACION", self.esperar(TokenType.IDENTIFICADOR).valor)
        self.esperar(TokenType.ASIGNACION)
        n.agregar_hijo(self.parse_expresion())
        self.esperar(TokenType.PUNTO_COMA)
        return n
        
    def parse_impresion(self):
        self.esperar(TokenType.PRINT)
        self.esperar(TokenType.PARENTESIS_IZQ)
        if self.actual().tipo == TokenType.CADENA: n = ASTNode("IMPRIMIR_CADENA", self.esperar(TokenType.CADENA).valor)
        else: n = ASTNode("IMPRIMIR_VAR", self.esperar(TokenType.IDENTIFICADOR).valor)
        self.esperar(TokenType.PARENTESIS_DER)
        self.esperar(TokenType.PUNTO_COMA)
        return n
        
    def parse_while(self):
        n = ASTNode("WHILE")
        self.esperar(TokenType.WHILE)
        self.esperar(TokenType.PARENTESIS_IZQ)
        n.agregar_hijo(self.parse_condicion())
        self.esperar(TokenType.PARENTESIS_DER)
        self.esperar(TokenType.LLAVE_IZQ)
        b = ASTNode("BLOQUE")
        while self.actual().tipo != TokenType.LLAVE_DER: b.agregar_hijo(self.parse_sentencia())
        self.esperar(TokenType.LLAVE_DER)
        n.agregar_hijo(b)
        return n
        
    def parse_if(self):
        n = ASTNode("IF")
        self.esperar(TokenType.IF)
        self.esperar(TokenType.PARENTESIS_IZQ)
        n.agregar_hijo(self.parse_condicion())
        self.esperar(TokenType.PARENTESIS_DER)
        self.esperar(TokenType.LLAVE_IZQ)
        b = ASTNode("BLOQUE_IF")
        while self.actual().tipo != TokenType.LLAVE_DER: b.agregar_hijo(self.parse_sentencia())
        self.esperar(TokenType.LLAVE_DER)
        n.agregar_hijo(b)
        if self.coincidir(TokenType.ELSE):
            self.esperar(TokenType.LLAVE_IZQ)
            be = ASTNode("BLOQUE_ELSE")
            while self.actual().tipo != TokenType.LLAVE_DER: be.agregar_hijo(self.parse_sentencia())
            self.esperar(TokenType.LLAVE_DER)
            n.agregar_hijo(be)
        return n
        
    def parse_return(self):
        self.esperar(TokenType.RETURN)
        n = ASTNode("RETURN")
        if self.actual().tipo != TokenType.PUNTO_COMA:
            n.agregar_hijo(self.parse_expresion())
        self.esperar(TokenType.PUNTO_COMA)
        return n
        
    def parse_condicion(self):
        n = ASTNode("CONDICION")
        n.agregar_hijo(self.parse_expresion())
        op = self.actual()
        if op.tipo in [TokenType.MENOR_QUE, TokenType.MAYOR_QUE, TokenType.IGUAL]:
            self.pos += 1
            n.valor = op.valor
        n.agregar_hijo(self.parse_expresion())
        return n
        
    def parse_expresion(self):
        izq = self.actual()
        if izq.tipo in [TokenType.NUMERO, TokenType.IDENTIFICADOR]:
            self.pos += 1
            n_izq = ASTNode("TERMINO", izq.valor)
            op = self.actual()
            if op.tipo in [TokenType.SUMA, TokenType.RESTA, TokenType.MULTIPLICACION, TokenType.DIVISION]:
                self.pos += 1
                n_op = ASTNode("OPERACION", op.valor)
                n_op.agregar_hijo(n_izq)
                der = self.actual()
                if der.tipo in [TokenType.NUMERO, TokenType.IDENTIFICADOR]:
                    self.pos += 1
                    n_op.agregar_hijo(ASTNode("TERMINO", der.valor))
                    return n_op
            return n_izq
        raise SyntaxError(f"Error de Sintaxis en la línea {izq.linea}: Expresión inválida cerca de '{izq.valor}'")