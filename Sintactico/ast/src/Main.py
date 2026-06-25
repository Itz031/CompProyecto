import sys, re

class ASTNode:
    def __init__(self, tipo, valor=None):
        self.tipo, self.valor, self.children = tipo, valor, []
    def add_child(self, child):
        if child: self.children.append(child)
    def print_node(self, padding=""):
        val = f": {self.valor}" if self.valor else ""
        print(f"{padding}└── [{self.tipo}{val}]")
        for c in self.children: c.print_node(padding + "    ")

class Token:
    def __init__(self, tipo, valor): self.tipo, self.valor = tipo, valor

def lexer(ruta):
    with open(ruta, 'r') as f: c = f.read()
    tokens = []
    pats = r'("[^"]*"|[a-zA-Z_]\w*|[0-9]+|[=+\-*/<>!&|]+|[;(),{}])'
    for m in re.finditer(pats, c):
        p = m.group(0)
        if p == "public": tokens.append(Token("PUBLIC", p))
        elif p == "class": tokens.append(Token("CLASS", p))
        elif p == "int": tokens.append(Token("DATATYPE", p))
        elif p == ";": tokens.append(Token("SEMICOLON", p))
        elif p == "{": tokens.append(Token("LBRACE", p))
        elif p == "}": tokens.append(Token("RBRACE", p))
        elif re.match(r'^[a-zA-Z_]\w*$', p): tokens.append(Token("IDENTIFIER", p))
        elif re.match(r'^\d+$', p): tokens.append(Token("NUMBER", p))
        elif re.match(r'^[=+\-*/]+$', p): tokens.append(Token("OPERATOR", p))
    tokens.append(Token("EOF", "EOF"))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens, self.table = tokens, {}
        self.rule("PROGRAM", "PUBLIC", ["PUBLIC", "CLASS", "IDENTIFIER", "LBRACE", "DATATYPE", "IDENTIFIER", "OPERATOR", "NUMBER", "SEMICOLON", "RBRACE"])
    def rule(self, nt, t, prod):
        if nt not in self.table: self.table[nt] = {}
        self.table[nt][t] = prod
    def parse(self):
        root = ASTNode("PROGRAM")
        stack = [("EOF", None), ("PROGRAM", root)]
        curr = 0
        while stack:
            top, parent = stack.pop()
            lookahead = self.tokens[curr]
            if top in ["PUBLIC", "CLASS", "IDENTIFIER", "LBRACE", "DATATYPE", "OPERATOR", "NUMBER", "SEMICOLON", "RBRACE", "EOF"]:
                if top == lookahead.tipo:
                    if parent and lookahead.tipo != "EOF": parent.add_child(ASTNode(lookahead.tipo, lookahead.valor))
                    curr += 1
            else:
                for s in reversed(self.table.get(top, {}).get(lookahead.tipo, [])):
                    n = ASTNode(top)
                    if parent: parent.add_child(n)
                    stack.append((s, n))
        return root

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Parser(lexer(sys.argv[1])).parse().print_node()