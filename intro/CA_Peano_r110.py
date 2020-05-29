# AC SOBRE UNA GEOMETRÍA DE UNA CURVAS DE PEANO QUE USA LA REGLA 110
# 111 -> 0
# 110 -> 1
# 101 -> 1
# 100 -> 0
# 011 -> 1
# 010 -> 1
# 001 -> 1
# 000 -> 0

import turtle
import collections # circular buffer: anillo
import random # entradas aleatorias
import time # esperar

def transitionFunctionRule110(ngbhood):
    ''' ngbhood es una lista de longitud 3, cada entrada es True o False'''
    if ngbhood[0] == True and ngbhood[1] == True and ngbhood[2] == True:
        return False
    elif ngbhood[0] == True and ngbhood[1] == True and ngbhood[2] == False:
        return True
    elif ngbhood[0] == True and ngbhood[1] == False and ngbhood[2] == True:
        return True
    elif ngbhood[0] == True and ngbhood[1] == False and ngbhood[2] == False:
        return False
    elif ngbhood[0] == False and ngbhood[1] == True and ngbhood[2] == True:
        return True
    elif ngbhood[0] == False and ngbhood[1] == True and ngbhood[2] == False:
        return True
    elif ngbhood[0] == False and ngbhood[1] == False and ngbhood[2] == True:
        return True
    elif ngbhood[0] == False and ngbhood[1] == False and ngbhood[2] == False:
        return False

def get_ngbhood(config_CA, pos):
    ''' confic_CA es una lista booleana
    la función regresa la vecindad dependiendo de la ubicación'''
    len_CA = len(config_CA)
    vec_ngb = [(pos - 1)% len_CA, pos % len_CA, (pos + 1) % len_CA]
    ngbhood = [config_CA[vec] for vec in vec_ngb]
    return ngbhood

def productionsHilbertCurve(chr):
    if chr == "A":
        return "−BF+AFA+FB−"
    elif chr == "B":
        return "+AF−BFB−FA+"
    return chr

def PeanoCurve(n_iter):
    ''' size_m es el tamaño de la matriz, debe ser un múltiplo de 3'''
    chain = "A"
    n_chain = ""
    for i in range(n_iter - 1):
        for chr in chain:
            n_chain += productionsHilbertCurve(chr)
        chain = n_chain
        n_chain = ""

    return chain

def n_rep_char(chain, chr):
    ''' función para contar el número de chr en chain '''
    count = 0
    for c in chain:
        if c == chr:
            count += 1
    return count

def get_CA_chain(chain, list_states):
    ''' función para crear la cadena que se usará como L-system'''
    CA_chain = ""
    it_CA = 0
    for chr in chain:
        if chr == "F":
            if list_states[it_CA]:
                CA_chain += "V" #vivo
            else:
                CA_chain += "M" # muerto
            it_CA += 1
        else:
            CA_chain += chr
    return CA_chain

def graphics(chain):
    ''' función que contiene todo lo necesario para crear los gráficos'''
    turtle.reset()
    #turtle.bgcolor("yellow")
    turtle.hideturtle()
    turtle.pensize(4)
    turtle.speed(0)
    turtle.setheading(90)
    turtle.tracer(0,0)
    turtle.color('green', 'yellow')
    for chr in chain:
        if chr == "V":
            turtle.pencolor("black")
            turtle.forward(10)
        if chr == "M":
            turtle.pencolor("red")
            turtle.forward(10)
        elif chr == "−":
            turtle.left(90)
        elif chr == "+":
            turtle.right(90)
    turtle.update()


if __name__ == "__main__":
    # n es el número de iteraciones
    n_iter = 6
    chain = PeanoCurve(6)
    n_lines = n_rep_char(chain, "F")
    n_evols = 500
    # dimensión del AC
    d_CA = n_lines

    list_states = [bool(random.getrandbits(1)) for x in range(d_CA)]

    CA_chain = get_CA_chain(chain, list_states)
    graphics(CA_chain)
    for j in range(n_evols):
        list_states = [transitionFunctionRule110(get_ngbhood(list_states,x)) for x in range(d_CA)]
        CA_chain = get_CA_chain(chain, list_states)
        graphics(CA_chain)
        time.sleep(0.5)

    turtle.done()
