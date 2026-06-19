import re
from TokenType import TokenType
from Token import Token

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.palabras_reservadas = {"int": TokenType.INT, "if": TokenType.IF, "else": TokenType.ELSE, "while": TokenType.WHILE, "print": TokenType.PRINT}
    def escanear_tokens(self):
        tokens = []
        patrones = [
            ('CADENA', r'".*?"'), ('NUMERO', r'\d+'), ('ID', r'[a-zA-Z_]\w*'),
            ('IGUAL', r'=='), ('ASIGNACION', r'='), ('SUMA', r'\+'), ('RESTA', r'-'),
            ('MULTIPLICACION', r'\*'), ('DIVISION', r'/'), ('MENOR_QUE', r'<'), ('MAYOR_QUE', r'>'),
            ('PARENTESIS_IZQ', r'\('), ('PARENTESIS_DER', r'\)'), ('LLAVE_IZQ', r'\{'),
            ('LLAVE_DER', r'\}'), ('PUNTO_COMA', r';'), ('WHITESPACE', r'\s+')
        ]
        regex = '|'.join(f'(?P<{n}>{p})' for n, p in patrones)
        for m in re.finditer(regex, self.codigo):
            t = m.lastgroup
            v = m.group(t)
            if t == 'WHITESPACE': continue
            if t == 'ID': tokens.append(Token(self.palabras_reservadas.get(v, TokenType.IDENTIFICADOR), v))
            elif t == 'CADENA': tokens.append(Token(TokenType.CADENA, v))
            else: tokens.append(Token(TokenType[t], v))
        tokens.append(Token(TokenType.EOF, "EOF"))
        return tokens