import sys
from AnalizadorLexico import AnalizadorLexico
from Parser import Parser
from GeneradorCodigo import GeneradorCodigo
from arbol import VisualizadorAST, EstadisticasAST, VisualizadorBinario

def compilar(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as f:
            codigo = f.read()
            
        print("=== 1. ANALISIS LEXICO ===")
        tokens = AnalizadorLexico(codigo).escanear_tokens()
        # for t in tokens: print(t)  # Puedes descomentar esto si quieres ver la lista de tokens
        print(f"[{len(tokens)} tokens generados]")
        
        print("\n=== 2. ANALISIS SINTACTICO (AST) ===")
        ast = Parser(tokens).parse()
        
        print("\n--- DETALLES DE EXPRESIONES BINARIAS ---")
        vis_binario = VisualizadorBinario()
        vis_binario.visualizar(ast)
        
        print("--- ESTRUCTURA COMPLETA DEL ARBOL ---")
        visualizador = VisualizadorAST()
        print(visualizador.visualizar(ast))
        
        estadisticas = EstadisticasAST()
        estadisticas.analizar(ast)
        print(estadisticas.obtener_reporte())
        
        print("\n=== 3. GENERACION DE CODIGO MASM ===")
        codigo_ensamblador = GeneradorCodigo(ast).generar()
        
        salida = ruta_archivo.replace(".c", ".asm")
        with open(salida, 'w') as f: f.write(codigo_ensamblador)
        print(f"ÉXITO: Ensamblador generado en '{salida}'")
        
    except SyntaxError as e:
        # ¡ESTO ATRAPA LOS ERRORES COMO EL PUNTO Y COMA FALTANTE!
        print(f"\n[✘] COMPILACIÓN DETENIDA: {e}")
    except Exception as e:
        print(f"\n[✘] Error del compilador: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: compilar(sys.argv[1])