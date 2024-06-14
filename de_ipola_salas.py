import lib
import random
import math
import matplotlib.pyplot as plt

def solucion_alternativa_1(ops = 1, TF=1, TR=8, N=7, S=3):
    t = 0
    broken_qty = 0

    while broken_qty <= S:
        if broken_qty == 0: # mecanico sin trabajar
            # Solo puede romperse una maquina, simulamos el tiempo y lo sumamos:
            t += random.expovariate(lambd=TF*N)
            broken_qty += 1

        else: # mecanico tiene al menos una maquina rota esperando
            # Pueden pasar dos cosas: una maquina se arregla u otra se rompe

            next_faliure_time = random.expovariate(lambd=TF*N) # tiempo hasta que se rompa otra maquina

            working = min(broken_qty, ops) # cantidad de maquinas que se estan reparando
            next_repair_time = random.expovariate(lambd=TR*working)   # tiempo hasta que se arregle una maquina

            if next_repair_time < next_faliure_time: # se arregla antes una caja
                t += next_repair_time
                broken_qty -= 1
            else:     # se rompe antes una caja
                t += next_faliure_time
                broken_qty += 1

    return t

def solucion_alternativa_2(ops = 1, TF=1, TR=8, N=7, S=3):

    # agregar tiempo de la primera falla
    t = 0
    broken_qty = 0

    while broken_qty <= S:
        # Generamos la siguiente falla
        next_failure_time = t + random.expovariate(lambd=TF*N)

        # Simulamos todas las reparaciones posibles antes de la siguiente falla
        while True:
            machines_being_repaired = min(broken_qty, ops)

            if machines_being_repaired == 0:
                break

            next_repair_time = t + random.expovariate(lambd=TR*machines_being_repaired)

            if next_repair_time < next_failure_time: # arreglamos antes
                broken_qty -= 1
                if broken_qty < 0:
                    raise Exception(f"Broken negativo: {broken_qty}")
                t = next_repair_time
            else: # se rompe antes otra maquina
                break
        t = next_failure_time
        broken_qty += 1

    return t

def solucion_sugerida(ops = 1, TF=1, TR=8, N=7, S=3):

    broken_qty = 0    # cantidad de cajas rotas
    t = 0    # tiempo transcurrido

    faliure_times = [random.expovariate(lambd=TF) for _ in range(N)]
    faliure_times.sort()

    repair_times = [math.inf] * ops


    while True:
        if faliure_times[0] < repair_times[0]: # Caso 1 
            t = faliure_times[0]
            broken_qty += 1
            if broken_qty == S+1:
                return t
            if broken_qty < S+1:
                x = random.expovariate(TF)
                faliure_times[0] = t + x
                faliure_times.sort()
            if math.inf in repair_times:
                y = random.expovariate(TR)
                index = repair_times.index(math.inf)
                repair_times[index] = t + y
                repair_times.sort()
        else:
            t = repair_times[0]
            broken_qty = broken_qty - 1
            working = len([x for x in repair_times if x != math.inf]) - 1
            available_work = broken_qty - working

            if available_work > 0:
                y = random.expovariate(TR)
                repair_times[0] = t + y
                repair_times.sort()
            if available_work == 0:
                repair_times[0] = math.inf
                repair_times.sort()
            if available_work < 0:
                raise Exception("Cantidad negativa de maquinas rotas: ", available_work, broken_qty, working, repair_times)



def gen_ej1(): return solucion_alternativa_1(ops=2)
def gen_ej2(): return solucion_alternativa_1(S=4)
def gen_ej1_2(): return solucion_sugerida(ops=2)
def gen_ej1_3(): return solucion_alternativa_2(ops=2)

n = 10_000

esp1,var = lib.sim_esp_var(gen_ej1, n)
print(esp1, var)
esp2,var = lib.sim_esp_var(gen_ej2, n)
print(esp2, var)

plt.hist[esp1,esp2]
plt.show()
# esp,var = lib.sim_esp_var(gen_ej1_3, n)
# print(esp, var)
