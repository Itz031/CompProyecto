import re
from Catalogo import TokenType
from Token import Token

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.palabras_reservadas = {
            "int": TokenType.INT, "if": TokenType.IF, "else": TokenType.ELSE, 
            "while": TokenType.WHILE, "print": TokenType.PRINT, "return": TokenType.RETURN
        }
        
    def escanear_tokens(self):
        tokens = []
        linea_actual = 1  # Llevamos el conteo de la línea
        
        patrones = [
            ('CADENA', r'".*?"'), ('NUMERO', r'\d+'), ('ID', r'[a-zA-Z_]\w*'),
            ('IGUAL', r'=='), ('ASIGNACION', r'='), ('SUMA', r'\+'), ('RESTA', r'-'),
            ('MULTIPLICACION', r'\*'), ('DIVISION', r'/'), ('MENOR_QUE', r'<'), ('MAYOR_QUE', r'>'),
            ('PARENTESIS_IZQ', r'\('), ('PARENTESIS_DER', r'\)'), ('LLAVE_IZQ', r'\{'),
            ('LLAVE_DER', r'\}'), ('PUNTO_COMA', r';'), ('WHITESPACE', r'\s+'), ('COMMENT', r'//.*|/\*[\s\S]*?\*/')
        ]
        regex = '|'.join(f'(?P<{n}>{p})' for n, p in patrones)
        
        for m in re.finditer(regex, self.codigo):
            t = m.lastgroup
            v = m.group(t)
            
            if t in ['WHITESPACE', 'COMMENT']:
                linea_actual += v.count('\n')
                continue
                
            if t == 'ID': 
                tipo_real = self.palabras_reservadas.get(v, TokenType.IDENTIFICADOR)
                tokens.append(Token(tipo_real, v, linea_actual))
            elif t == 'CADENA': 
                tokens.append(Token(TokenType.CADENA, v, linea_actual))
            else: 
                tokens.append(Token(TokenType[t], v, linea_actual))
                
            linea_actual += v.count('\n')
            
        tokens.append(Token(TokenType.EOF, "EOF", linea_actual))
        return tokens