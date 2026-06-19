from enum import Enum, auto
class TokenType(Enum):
    INT = auto(); IF = auto(); ELSE = auto(); WHILE = auto(); PRINT = auto()
    IDENTIFICADOR = auto(); NUMERO = auto(); CADENA = auto()
    SUMA = auto(); RESTA = auto(); MULTIPLICACION = auto(); DIVISION = auto()
    ASIGNACION = auto(); MENOR_QUE = auto(); MAYOR_QUE = auto(); IGUAL = auto()
    PARENTESIS_IZQ = auto(); PARENTESIS_DER = auto()
    LLAVE_IZQ = auto(); LLAVE_DER = auto(); PUNTO_COMA = auto(); EOF = auto()