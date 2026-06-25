
class VisualizadorAST:
 
    def __init__(self):
        self.salida = []
    
    def visualizar(self, nodo):
        self.salida = []
        self._visitar(nodo, prefijo="", es_ultimo=True)
        return '\n'.join(self.salida)
    
    def _visitar(self, nodo, prefijo, es_ultimo):
        if nodo is None:
            return
            
        # Determinar el conector de la rama
        if prefijo == "":
            marcador = "┌─ "
        elif es_ultimo:
            marcador = "└─ "
        else:
            marcador = "├─ "
            
        # Personalizar el texto para dar el máximo detalle posible en el mismo árbol
        if nodo.tipo == "OPERACION":
            texto_nodo = f"[Expresión Binaria] Operador: '{nodo.valor}'"
        elif nodo.tipo == "ASIGNACION":
            texto_nodo = f"[Asignación] Objetivo: variable '{nodo.valor}'"
        elif nodo.tipo == "DECLARACION":
            texto_nodo = f"[Declaración] Nueva variable: '{nodo.valor}'"
        elif nodo.tipo == "TERMINO":
            # Intentar saber si es un número (constante) o una variable
            if str(nodo.valor).isdigit():
                texto_nodo = f"[Constante Numérica] {nodo.valor}"
            else:
                texto_nodo = f"[Variable] {nodo.valor}"
        elif nodo.tipo == "CONDICION":
            texto_nodo = f"[Condición Relacional] Operador: '{nodo.valor}'"
        else:
            texto_nodo = f"[{nodo.tipo}]"
            if nodo.valor is not None:
                texto_nodo += f" : {nodo.valor}"
                
        # Agregar a la salida
        self.salida.append(prefijo + marcador + texto_nodo)
        
        # Calcular los espacios para las sub-ramas
        if prefijo == "":
            nuevo_prefijo = "   "
        else:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            
        # Recorrer a todos los hijos (las ramas secundarias)
        for i, hijo in enumerate(nodo.hijos):
            es_el_ultimo_hijo = (i == len(nodo.hijos) - 1)
            self._visitar(hijo, nuevo_prefijo, es_el_ultimo_hijo)


class EstadisticasAST:
    """Calcula y formatea las estadísticas del AST"""
    def __init__(self):
        self.total_nodos = 0
        self.tipos_nodos = {}
        self.profundidad_maxima = 0
        self.profundidad_actual = 0
    
    def analizar(self, nodo):
        self.total_nodos, self.tipos_nodos, self.profundidad_maxima, self.profundidad_actual = 0, {}, 0, 0
        self._contar_nodos(nodo)
        return self
    
    def _contar_nodos(self, nodo):
        if nodo is None: return
        self.profundidad_actual += 1
        self.profundidad_maxima = max(self.profundidad_maxima, self.profundidad_actual)
        self.tipos_nodos[nodo.tipo] = self.tipos_nodos.get(nodo.tipo, 0) + 1
        self.total_nodos += 1
        for hijo in nodo.hijos: self._contar_nodos(hijo)
        self.profundidad_actual -= 1
    
    def obtener_reporte(self):
        reporte = ["\n" + "="*60, "ESTADÍSTICAS DEL AST", "="*60, f"Total de nodos: {self.total_nodos}", f"Profundidad máxima: {self.profundidad_maxima}", "\nTipos de nodos:"]
        for t, c in sorted(self.tipos_nodos.items()): reporte.append(f"  {t}: {c}")
        reporte.append("="*60)
        return '\n'.join(reporte)