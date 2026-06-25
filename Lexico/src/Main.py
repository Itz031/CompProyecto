import sys
import re

def escanear_codigo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            codigo = file.read()
    except FileNotFoundError:
        print(f"Error al leer '{ruta_archivo}'.")
        return

    reglas = {
        "IF": r"\bif\b", "ELSE": r"\belse\b", "WHILE": r"\bwhile\b",
        "INT": r"\bint\b", "PRINT": r"\bprint\b",
        "STRINGLITERAL": r'".*?"', "NUMERO": r"\d+",
        "OPERATOR": r"[+\-*/=<>!]+", "LPAREN": r"\(", "RPAREN": r"\)",
        "LBRACE": r"\{", "RBRACE": r"\}", "SEMICOLON": r";",
        "ID": r"[a-zA-Z_]\w*", "WHITESPACE": r"\s+", "UNKNOWN": r"."
    }

    regex = '|'.join(f'(?P<{n}>{p})' for n, p in reglas.items())
    print("--- Análisis Léxico ---")
    
    for match in re.finditer(regex, codigo):
        tipo = match.lastgroup
        lexema = match.group(tipo)
        if tipo not in ["WHITESPACE"]:
            print(f"<{tipo} | {lexema}>")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        escanear_codigo(sys.argv[1])