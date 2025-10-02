class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("La pila está vacía")

    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

def postfija_a_prefija(expresion):
    pila = Pila()
    for simbolo in expresion.split():
        if simbolo.isdigit():
            pila.apilar(simbolo)
        else:
            op2 = pila.desapilar()
            op1 = pila.desapilar()
            pila.apilar(simbolo + " " + op1 + " " + op2)
    return pila.desapilar()

def prefija_a_postfija(expresion):
    pila = Pila()
    for simbolo in expresion.split()[::-1]:
        if simbolo.isdigit():
            pila.apilar(simbolo)
        else:
            op1 = pila.desapilar()
            op2 = pila.desapilar()
            pila.apilar(op1 + " " + op2 + " " + simbolo)
    return pila.desapilar()

def postfija_a_infija(expresion):
    pila = Pila()
    for simbolo in expresion.split():
        if simbolo.isdigit():
            pila.apilar(simbolo)
        else:
            op2 = pila.desapilar()
            op1 = pila.desapilar()
            pila.apilar(f"( {op1} {simbolo} {op2} )")
    return pila.desapilar()

def prefija_a_infija(expresion):
    pila = Pila()
    for simbolo in expresion.split()[::-1]:
        if simbolo.isdigit():
            pila.apilar(simbolo)
        else:
            op1 = pila.desapilar()
            op2 = pila.desapilar()
            pila.apilar(f"( {op1} {simbolo} {op2} )")
    return pila.desapilar()

def infija_a_postfija(expresion):
    prec = {'+':1, '-':1, '*':2, '/':2}
    salida = []
    pila = Pila()
    for token in expresion.split():
        if token.isdigit():
            salida.append(token)
        elif token in '+-*/':
            while not pila.esta_vacia() and pila.ver_tope() != '(' and prec[pila.ver_tope()] >= prec[token]:
                salida.append(pila.desapilar())
            pila.apilar(token)
        elif token == '(':
            pila.apilar(token)
        elif token == ')':
            while not pila.esta_vacia() and pila.ver_tope() != '(':
                salida.append(pila.desapilar())
            pila.desapilar()
    while not pila.esta_vacia():
        salida.append(pila.desapilar())
    return ' '.join(salida)

def infija_a_prefija(expresion):
    post = infija_a_postfija(expresion)
    return postfija_a_prefija(post)


def evaluar_postfija(expresion):
    pila = Pila()
    for simbolo in expresion.split():
        if simbolo.isdigit():
            pila.apilar(int(simbolo))
        else:
            op2 = pila.desapilar()
            op1 = pila.desapilar()
            if simbolo == '+': pila.apilar(op1 + op2)
            elif simbolo == '-': pila.apilar(op1 - op2)
            elif simbolo == '*': pila.apilar(op1 * op2)
            elif simbolo == '/': pila.apilar(op1 / op2)
    return pila.desapilar()

def evaluar_prefija(expresion):
    pila = Pila()
    for simbolo in expresion.split()[::-1]:
        if simbolo.isdigit():
            pila.apilar(int(simbolo))
        else:
            op1 = pila.desapilar()
            op2 = pila.desapilar()
            if simbolo == '+': pila.apilar(op1 + op2)
            elif simbolo == '-': pila.apilar(op1 - op2)
            elif simbolo == '*': pila.apilar(op1 * op2)
            elif simbolo == '/': pila.apilar(op1 / op2)
    return pila.desapilar()

def evaluar_infija(expresion):
    post = infija_a_postfija(expresion)
    return evaluar_postfija(post)


if __name__ == "__main__":
    expresion = input("Ingresa la expresión (usa espacios entre símbolos y paréntesis si infija): ")
    tokens = expresion.split()

    if tokens[0] in "+-*/":  # Prefija
        print("\nLa expresión es PREFIJA.")
        print("Postfija:", prefija_a_postfija(expresion))
        print("Infija:", prefija_a_infija(expresion))

    elif tokens[-1] in "+-*/":  # Postfija
        print("\nLa expresión es POSTFIJA.")
        print("Prefija:", postfija_a_prefija(expresion))
        print("Infija:", postfija_a_infija(expresion))

    else:  # Infija
        print("\nLa expresión es INFÍJA.")
        print("Postfija:", infija_a_postfija(expresion))
        print("Prefija:", infija_a_prefija(expresion))