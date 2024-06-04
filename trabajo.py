import random
import lib


def sim(R = 1, TF=1, TR=8, N=7, S=3):
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

def gen_ej1(): return sim()
def gen_ej2(): return sim(R=2)

n = 100_000

esp,var = lib.sim_esp_var(gen_ej1, n)
print(esp, var)
esp,var = lib.sim_esp_var(gen_ej2, n)
print(esp, var)
