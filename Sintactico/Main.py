import sys
from AnalizadorLexico import AnalizadorLexico
from Parser import Parser
from GeneradorCodigo import GeneradorCodigo
from arbol import VisualizadorAST, EstadisticasAST

def compilar(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as f:
            codigo = f.read()
            
        print("------- ANALISIS LEXICO ------")
        tokens = AnalizadorLexico(codigo).escanear_tokens()
        print(f"[{len(tokens)} tokens generados]")
        
        print("\n----- ANALISIS SINTACTICO (AST) -----")
        ast = Parser(tokens).parse()
        
        # Muestra el árbol unificado gigante
        print("---- ESTRUCTURA COMPLETA DEL ARBOL ---")
        visualizador = VisualizadorAST()
        print(visualizador.visualizar(ast))
        
        # Muestra las estadísticas
        estadisticas = EstadisticasAST()
        estadisticas.analizar(ast)
        print(estadisticas.obtener_reporte())
        
        print("\n----- GENERACION DE CODIGO MASM ------")
        codigo_ensamblador = GeneradorCodigo(ast).generar()
        
        salida = ruta_archivo.replace(".c", ".asm")
        with open(salida, 'w') as f: f.write(codigo_ensamblador)
        print(f"ÉXITO: Ensamblador generado en '{salida}'")
        
    except SyntaxError as e:
        print(f"\n[✘] COMPILACIÓN DETENIDA: {e}")
    except Exception as e:
        print(f"\n[✘] Error del compilador: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: compilar(sys.argv[1])