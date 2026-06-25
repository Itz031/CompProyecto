class GeneradorCodigo:
    def __init__(self, ast_root):
        self.ast = ast_root
        self.seccion_datos = ".data\n"
        self.seccion_codigo = ".code\nstart:\n"
        self.contador_etiquetas = 0
        self.contador_cadenas = 0
        self.variables_declaradas = set()

    def nueva_etiqueta(self):
        self.contador_etiquetas += 1
        return f"Label_{self.contador_etiquetas}"

    def generar(self):
        self.visitar_nodo(self.ast)
        
        # En MASM ya no ponemos el ExitProcess fijo aquí, porque C tiene el "return 0;"
        self.seccion_codigo += "end start\n"
        
        encabezado = (
            ".386\n.model flat, stdcall\noption casemap :none\n"
            "include \\masm32\\include\\windows.inc\n"
            "include \\masm32\\include\\kernel32.inc\n"
            "include \\masm32\\include\\masm32.inc\n"
            "includelib \\masm32\\lib\\kernel32.lib\n"
            "includelib \\masm32\\lib\\masm32.lib\n\n"
        )
        self.seccion_datos += "    buffer db 20 dup(0)\n    fmt db '%d', 10, 13, 0\n"
        return encabezado + self.seccion_datos + "\n" + self.seccion_codigo

    def visitar_nodo(self, nodo):
        if nodo.tipo in ["PROGRAMA", "BLOQUE", "BLOQUE_IF", "BLOQUE_ELSE"]:
            for h in nodo.hijos: self.visitar_nodo(h)
            
        elif nodo.tipo == "FUNCION":
            # Es el main(). Visitamos su cuerpo (BLOQUE)
            self.visitar_nodo(nodo.hijos[0])
            
        elif nodo.tipo == "RETURN":
            # El return de C se traduce al ExitProcess de Ensamblador
            self.seccion_codigo += "    invoke ExitProcess, 0\n"
            
        elif nodo.tipo == "DECLARACION":
            nombre = nodo.valor
            if nombre not in self.variables_declaradas:
                self.seccion_datos += f"    {nombre} DWORD 0\n"
                self.variables_declaradas.add(nombre)
            if nodo.hijos:
                self.evaluar_expresion(nodo.hijos[0])
                self.seccion_codigo += f"    mov {nombre}, eax\n"
                
        elif nodo.tipo == "ASIGNACION":
            if nodo.valor not in self.variables_declaradas:
                raise Exception(f"Error Semántico: La variable '{nodo.valor}' no ha sido declarada.")
            self.evaluar_expresion(nodo.hijos[0])
            self.seccion_codigo += f"    mov {nodo.valor}, eax\n"
            
        elif nodo.tipo == "IMPRIMIR_VAR":
            self.seccion_codigo += f"    invoke wsprintf, addr buffer, addr fmt, {nodo.valor}\n    invoke StdOut, addr buffer\n"
        elif nodo.tipo == "IMPRIMIR_CADENA":
            self.contador_cadenas += 1
            nombre = f"str_{self.contador_cadenas}"
            val = nodo.valor.replace('"', '')
            self.seccion_datos += f"    {nombre} db '{val}', 10, 13, 0\n"
            self.seccion_codigo += f"    invoke StdOut, addr {nombre}\n"
        elif nodo.tipo == "WHILE":
            inicio, fin = self.nueva_etiqueta() + "_WHILE_INICIO", self.nueva_etiqueta() + "_WHILE_FIN"
            self.seccion_codigo += f"{inicio}:\n"
            self.evaluar_condicion(nodo.hijos[0], fin, True)
            self.visitar_nodo(nodo.hijos[1])
            self.seccion_codigo += f"    jmp {inicio}\n{fin}:\n"
        elif nodo.tipo == "IF":
            fin = self.nueva_etiqueta() + "_IF_FIN"
            else_lbl = self.nueva_etiqueta() + "_ELSE" if len(nodo.hijos) > 2 else fin
            self.evaluar_condicion(nodo.hijos[0], else_lbl, True)
            self.visitar_nodo(nodo.hijos[1])
            if len(nodo.hijos) > 2:
                self.seccion_codigo += f"    jmp {fin}\n{else_lbl}:\n"
                self.visitar_nodo(nodo.hijos[2])
            self.seccion_codigo += f"{fin}:\n"

    def evaluar_expresion(self, nodo):
        if nodo.tipo == "TERMINO": self.seccion_codigo += f"    mov eax, {nodo.valor}\n"
        elif nodo.tipo == "OPERACION":
            self.evaluar_expresion(nodo.hijos[0])
            self.seccion_codigo += "    mov ebx, eax\n"
            self.evaluar_expresion(nodo.hijos[1])
            if nodo.valor == '+': self.seccion_codigo += "    add eax, ebx\n"
            elif nodo.valor == '-': self.seccion_codigo += "    sub ebx, eax\n    mov eax, ebx\n"
            elif nodo.valor == '*': self.seccion_codigo += "    imul eax, ebx\n"

    def evaluar_condicion(self, condicion, destino, salto_si_falso=True):
        self.evaluar_expresion(condicion.hijos[0])
        self.seccion_codigo += "    mov ecx, eax\n"
        self.evaluar_expresion(condicion.hijos[1])
        self.seccion_codigo += "    cmp ecx, eax\n"
        if condicion.valor == '<': jmp = "jge" if salto_si_falso else "jl"
        elif condicion.valor == '>': jmp = "jle" if salto_si_falso else "jg"
        else: jmp = "jne" if salto_si_falso else "je"
        self.seccion_codigo += f"    {jmp} {destino}\n"