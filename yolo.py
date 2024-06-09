import lib
import random
import math

def sim_original(R = 1, TF=1, TR=8, N=7, S=3):
    """
    Simula el tiempo de crash del supermercado del enunciado del problema 3

    Por defecto simula el tiempo del ejercicio 1.

    Si le pasamos R = 2 (dos reparadores) simula el tiempo del ejercicio 2

    R: cantidad de operadores
    TF: tasa de fallo
    TR: tasa de reparacion de un operario
    N: cantidad de maquinas necesarias para el funcionamiento
    S: cantidad de maquinas de repuesto
    """
    t = 0
    B=0

    while B <= S:
        if B == 0: # mecanico sin trabajar
            # Solo puede romperse una maquina, simulamos el tiempo y lo sumamos:
            t += random.expovariate(lambd=TF*N)
            B += 1

        else: # mecanico tiene al menos una maquina rota esperando
            # Pueden pasar dos cosas: una maquina se arregla u otra se rompe

            x = random.expovariate(lambd=TF*N) # tiempo hasta que se rompa otra maquina

            M = min(B, R) # cantidad de maquinas que se estan reparando
            y = random.expovariate(lambd=TR*M)   # tiempo hasta que se arregle una maquina

            if y < x: # se arregla antes una caja
                t += y
                B -= 1
            else:     # se rompe antes una caja
                t += x
                B += 1

    return t

def sim(ops = 1, TF=1, TR=8, N=7, S=3):

    # agregar tiempo de la primera falla
    t = 0
    broken = 0

    while broken <= S:
        # Generamos la siguiente falla
        next_failure_time = t + random.expovariate(lambd=TF*N)

        # Simulamos todas las reparaciones posibles antes de la siguiente falla
        while True:
            machines_being_repaired = min(broken, ops)

            if machines_being_repaired == 0:
                break

            next_repair_time = t + random.expovariate(lambd=TR*machines_being_repaired)

            if next_repair_time < next_failure_time: # arreglamos antes
                broken -= 1
                if broken < 0:
                    raise Exception(f"Broken negativo: {broken}")
                t = next_repair_time
            else: # se rompe antes otra maquina
                break
        t = next_failure_time
        broken += 1

    return t
def sim_ross(ops = 1):
    TF = 1 # tasa de fallo
    TR = 8 # tasa de reparacion
    N = 7  # cantidad de cajas
    S = 3  # cantidad de repuestos
    r = 0    # cantidad de cajas rotas
    t = 0    # tiempo transcurrido

    ts = [random.expovariate(lambd=TF) for _ in range(N)]
    ts.sort()

    tr = [math.inf] * ops


    while True:
        if ts[0] < tr[0]: # Caso 1 de Ross
            t = ts[0]
            r += 1
            if r == S+1:
                return t
            if r < S+1:
                x = random.expovariate(TF)
                ts[0] = t + x
                ts.sort()
            if math.inf in tr:
                y = random.expovariate(TR)
                index = tr.index(math.inf)
                tr[index] = t + y
                tr.sort()
        else:
            t = tr[0]
            r = r - 1
            working = len([x for x in tr if x != math.inf]) - 1
            available_work = r - working

            if available_work > 0:
                y = random.expovariate(TR)
                tr[0] = t + y
                tr.sort()
            if available_work == 0:
                tr[0] = math.inf
                tr.sort()
            if available_work < 0:
                raise Exception("Cantidad negativa de maquinas rotas: ", available_work, r, working, tr)




# sim_ross(ops=2)
def gen_ej1(): return sim(ops=2)
def gen_ej1_2(): return sim_ross(ops=2)
def gen_ej1_3(): return sim_original(R=2)

n = 10_000

esp,var = lib.sim_esp_var(gen_ej1, n)
print(esp, var)
esp,var = lib.sim_esp_var(gen_ej1_2, n)
print(esp, var)
esp,var = lib.sim_esp_var(gen_ej1_3, n)
print(esp, var)
