########
####### DILEMA DEL PRISIONERO
########
# # dos jugadores identificados por su número
# N = 2
# A = [["D", "ND"],
#     ["D", "ND"]]
#
# # u_1 = {("D","D"): -10, ("ND","D"): -15,("D","ND"): 0,("ND","ND"): -1}
# # u_2 = {("D","D"): -10, ("ND","D"): 0,("D","ND"): -15,("ND","ND"): -1}
#
# u = {("D","D"): (-10,-10), ("ND","D"): (-15,0),
#         ("D","ND"): (0,-15),("ND","ND"): (-1,-1)}


########
####### STRAFFIN. P65
########
N = 2
A = [["A", "B"],
    ["A", "B"]]

u = {("A","A"): (2,4), ("B","A"): (3,1),
        ("A","B"): (1,0),("B","B"): (0,4)}



##########################################################################     b
# dominated = -1
# isStrict = False
# # aún no sabemos si no existen estrategias dominadas
# # el ciclo terminará cuando no existan
# notDominatedStr = False
# # contador de los jugador analizado
# c_players = 0
#
# # contador del num de jugadores sin estrategias dominadas
# n_pwds = 0

# eliminate dominated stategies
# a dominated by a_1
# for a_1 in A[1]:
#     for a in A[1]:
#         if a != a_1:
#             # otro jugador
#             for row in A[0]:
#                 # a dominated by a_1
#                 if u[(row,a_1)][1] > u[(row,a)][1]:
#                     isStrict = True
#                     dominated = a
#
#                 # si una de las estrategias para a_1 tiene una recompensa menor
#                 # que para a, entonces ya no es estricto y no se puede eliminar
#                 elif u[(row,a_1)][1] < u[(row,a)][1]:
#                     isStrict = False
#                     dominated = -1
#                     # romper el ciclo por que la siguente entrada para a_1 puede
#                     # cumplir la condición de dominación sobre a
#                     break
#
#         # nos interesa solo la primera estrategia dominada
#         if dominated != -1:
#             break
#     if dominated != -1:
#         break
#
# print(dominated)
#
# if dominated != -1:
#     # eliminamos la correspondiente fila/columna
#     A_1 = [A[0],[]]
#     for strat in A[1]:
#         if strat != dominated:
#             A_1[1].append(strat)
#
#     dominated = -1
#
# print(A_1)
# A= A_1

###################################     u

dominated = -1
isStrict = False
# aún no sabemos si no existen estrategias dominadas
# el ciclo terminará cuando no existan
notDominatedStr = False
# contador de los jugador analizado
c = 0

# contador del num de jugadores sin estrategias dominadas
n_pwds = 0



while(not notDominatedStr):


    # el jugador es c
    # a dominada por a_1
    for a_1 in A[c]:
        for a in A[c]:
            if a != a_1:
                # otro jugador, (c+1) % N-> c =0: 1; c =1: 0.
                # válido solo cuando N = 2
                # b -> strategies of the other player
                #for row in A[(c+1)%c]:
                for b in A[(c+1) % N]:
                    # lista para considerar la posición de las estrategias
                    l_st_ab = [0,0]
                    l_st_a_1b = [0,0]
                    l_st_ab[c] = a
                    l_st_a_1b[c] = a_1

                    l_st_ab[(c+1) % N] = b
                    l_st_a_1b[(c+1) % N] = b

                    # convertir a tuplas
                    t_st_ab = tuple(l_st_ab)
                    t_st_a_1b = tuple(l_st_a_1b)


                    # a dominated by a_1
                    if u[t_st_a_1b][c] > u[t_st_ab][c]:
                        isStrict = True
                        dominated = a

                    # si una de las estrategias para a_1 tiene una recompensa menor
                    # que para a, entonces ya no es estricto y no se puede eliminar
                    elif u[t_st_a_1b][c] < u[t_st_ab][c]:
                        isStrict = False
                        dominated = -1
                        # romper el ciclo por que la siguente entrada para a_1 puede
                        # cumplir la condición de dominación sobre a
                        break

            # nos interesa solo la primera estrategia dominada
            if dominated != -1:
                break
        if dominated != -1:
            break


    if dominated != -1:
        # eliminamos la correspondiente fila/columna
        A_1 = [[],[]]
        #A_1 = [A[0],[]]   # <-
        # se mantienen las estrategias del oponente
        A_1[(c+1) % N] = A[(c+1) % N]
        # se modifican las del jugador actual
        for strat in A[c]:
            if strat != dominated:
                A_1[c].append(strat) # <-

        # igualamos para guardar el cambio
        A = A_1
        n_pwds = 0
        dominated = -1

    # si no hay estrategias dominadas para un jugador
    # pasa a analizar al siguiente jugador
    else:
        n_pwds += 1


    # aumenta el contador de jugadores, pero en módulo
    c = (c + 1) % N

    # si el número de jugadores analizados es igual al número de jugadores
    # participantes, no hay estrategias dominadas
    if n_pwds == N:
        notDominatedStr = True

print(A)
