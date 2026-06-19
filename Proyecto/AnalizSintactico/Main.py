import sys
from AnalizadorLexico import AnalizadorLexico
from Parser import Parser
from GeneradorCodigo import GeneradorCodigo

def compilar(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as f:
            codigo = f.read()
        print("=== 1. ANALISIS LEXICO ===")
        tokens = AnalizadorLexico(codigo).escanear_tokens()
        for t in tokens: print(t)
        
        print("\n=== 2. ANALISIS SINTACTICO (AST) ===")
        ast = Parser(tokens).parse()
        ast.imprimir_arbol()
        
        print("\n=== 3. GENERACION DE CODIGO MASM ===")
        codigo_ensamblador = GeneradorCodigo(ast).generar()
        
        salida = ruta_archivo.replace(".c", ".asm")
        with open(salida, 'w') as f: f.write(codigo_ensamblador)
        print(f"ÉXITO: Ensamblador generado en '{salida}'")
    except Exception as e:
        print(f"Error de compilación: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: compilar(sys.argv[1])