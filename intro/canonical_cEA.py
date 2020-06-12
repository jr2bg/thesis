# dependencies
import numpy as np
import random
# animation
import pygame

def fitness(cell):
    # si solo regresa cell, significa que está trabajando sobre una
    # función lineal

    return cell

def fitness_ratio(population_fitness):
    ''' función que calcula el cociente del fitness de toda la población'''
    total = sum(population_fitness)
    l_f_ratio = [x/total for x in population_fitness]
    return l_f_ratio

def a_fit_ratio(l_fit_ratio):
    ''' función que regresa el acumulado de la lista con los valores de fitness'''
    # como en programación dinámica
    accum_fit_ratio = [(0,l_fit_ratio[0])]
    # se toma desde el inicio hasta el final, por eso es que es una tupla
    for fit in l_fit_ratio[1:]:
        accum_fit_ratio.append((accum_fit_ratio[-1][1],accum_fit_ratio[-1][1] + fit))

    return accum_fit_ratio

def parents_selection(accum_fit_ratio):
    ''' función que regresa a los progenitores '''
    # se usa la 'ruleta'
    pos_parents = []
    # REEMPLAZO
    # número aleatorio para saber qué padres escoger
    point = random.random()
    if point <= 0.5:
        n_point = point + 0.5
    else:
        n_point = point - 0.5
    for i in range(len(accum_fit_ratio)):
        if  accum_fit_ratio[i][0] <= point <= accum_fit_ratio[i][1]:
            pos_parents.append(i)
        if accum_fit_ratio[i][0] <= n_point <= accum_fit_ratio[i][1]:
            pos_parents.append(i)

    return pos_parents

def crossover(f_parent, s_parent):
    ''' función para el intercambio de cromosomas entre los padres
     toma la mitad de uno y la reemplaza en la otra mitad'''
    l_cut = len(f_parent) // 2
    r_cut = len(f_parent) - l_cut

    f_child = f_parent[:l_cut] + s_parent[l_cut:]
    s_child = s_parent[:l_cut] + f_parent[l_cut:]
    return f_child, s_child

def mutation(child, p_m):
    ''' función de mutación con probabilidad p_m'''
    child = list(child) # cadenas son inmutables, necesario pasar a lista
    for i in range(len(child)):
        if random.random() <= p_m:
            if child[i] == "0":
                child[i] = "1"
            else:
                child[i] = "0"
    child = "".join(child)  # lo regresa un str
    return child


class CEA:
    def __init__(self, n_cols, n_rows, mutation_prob = 0.001):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = np.zeros([n_rows,n_cols])
        self.p_m = mutation_prob

    def init_population(self):
        ''' inicializa la teselación con valores enteros entre 0 y 255'''
        with np.nditer(self.grid, op_flags = ['readwrite']) as it:
            for cell in it:
                cell[...] = random.randint(0 , 255)
        print(self.grid)

    def neigh(self,cell_pos):
        ''' método para extraer la vecindad alrededor de una célula del CA'''
        # creación del toroide
        neigh_rows = [(cell_pos[0] - 1) % self.n_rows, cell_pos[0]% self.n_rows,
                    (cell_pos[0] + 1)% self.n_rows]
        neigh_cols = [(cell_pos[1] - 1)% self.n_cols, cell_pos[1]% self.n_cols,
                    (cell_pos[1] + 1)% self.n_cols]

        nbg_np = self.grid[np.ix_(neigh_rows, neigh_cols)]
        ngb_l = list(np.concatenate(nbg_np).flat)
        # lista no anidada
        return ngb_l


    def evolution(self):
        ''' regla de evolución, iteración sobre cada elemento del grid'''
        #print("--- NEIGHBORHOODS---")
        with np.nditer(self.grid, op_flags = ['readwrite']) as it:
            # contador de la iteración sobre el arreglo de numpy
            i = 0
            for cell in it:
                l_fitness = [] # lista con el fitness de la vecindad

                # posición de la celda con respecto al número de iteraciones
                # sobre el arreglo del numpy
                cell_pos = (i// self.n_cols, i%self.n_cols)

                # numpy solo trabaja con floats, necesario pasarlo a int
                int_cell = int(cell)
                # vecindad como un arreglo plano
                ngbhood = self.neigh(cell_pos)

                for habitant in ngbhood:
                    l_fitness.append(fitness(habitant))
                #print(ngbhood)

                # determinación de las probabilidades para seleccionar los padres
                l_fitness = fitness_ratio(l_fitness)
                l_fitness = a_fit_ratio(l_fitness)

                # obtención de la posición de los padres
                pos_parents = parents_selection(l_fitness)

                # identificación de los padres y codeado a binario
                f_parent = bin(int(ngbhood[pos_parents[0]]))
                s_parent = bin(int(ngbhood[pos_parents[1]]))

                # remover el "0b" inicial del str
                f_parent = f_parent[2:]
                s_parent = s_parent[2:]

                #crossover
                f_child, s_child = crossover(f_parent, s_parent)

                #mutation
                f_child = mutation(f_child, self.p_m)
                s_child = mutation(s_child, self.p_m)

                # reconstruction
                f_child = int(f_child, 2)
                s_child = int(s_child, 2)

                # assotiation of the cell with a value
                if fitness(f_child) > fitness(s_child):
                    cell[...] = f_child
                else:
                    cell[...] = s_child

                # print(l_fitness)
                # print(pos_parents)
                # print(f_parent, s_parent)
                # print(cell)
                # print("")

                i +=1


def main():
    '''  función principal a ejecutar
    contiene información acerca de las dimensiones del CA,
    así como de la condición de paro '''
    n_cols = 50
    n_rows = 40
    cea = CEA(n_cols, n_rows)
    cea.init_population()

    # VARIABLE INITIALIZATION FOR PYGAME
    white = (255, 255, 255)
    black = ( 0, 0, 0)
    gray = (165, 165, 165)
    tamCuadro = 20
    height = n_rows #num_cuadros altura
    width = n_cols  #num_cuadros ancho




    # VISUALIZATION
    pygame.init()
    pygame.event.pump()
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    size = ((tamCuadro + 1) * width, (tamCuadro + 1) * height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Grid on PYGAME")
    clock = pygame.time.Clock()
    FPS = 10    #frames per secont
    clock.tick(FPS)
    gameOver = False
    setup = True

    # condición de paro: 20 iteraciones
    n_it = 0

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
        screen.fill(gray)
        if n_it <= 20:
            cea.evolution()
            print(cea.grid)
        #config = iteration(config, height, width)
        wh = 0
        for i in range(1, size[0], tamCuadro + 1):   # width
            ht = 0
            for j in range(1, size[1], tamCuadro + 1): # height
                #// colores (0-7 azul) (8-15 verde) (16-23 rojo)
                cell_val = int(cea.grid[ht,wh])
                color = cell_val << 2 | cell_val << 9 | cell_val << 20
                pygame.draw.rect(screen, color,
                            [i, j, tamCuadro, tamCuadro], 0)
                ht += 1
            wh += 1
        pygame.display.flip()
        clock.tick(1)

        n_it += 1 # nueva iteración
        print(n_it)
    pygame.quit()
    print("SUCCESS")



if __name__ == "__main__":
    main()
