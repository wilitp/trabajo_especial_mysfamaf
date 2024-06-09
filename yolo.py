import lib
import random
import math

ns = {}

def sim(ops = 1, TF=1, TR=8, N=7, S=3):

    # agregar tiempo de la primera falla
    t = random.expovariate(TF*N)
    broken = 1

    while broken <= S:
        # Generamos la siguiente falla
        next_failure_time = t + random.expovariate(lambd=TF*N)

        # Simulamos todas las reparaciones posibles antes de la siguiente falla
        while True:
            machines_being_repaired = min(broken, ops)
            ns[machines_being_repaired] = ns.get(machines_being_repaired, 0) + 1

            if machines_being_repaired == 0:
                break

            next_repair_time = t + random.expovariate(lambd=TR*machines_being_repaired)

            if next_repair_time < next_failure_time: # arreglamos antes
                broken -= 1
                if broken < 0:
                    raise Exception(f"wtf{broken}")
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

    def add_repair_time(ti):
        nonlocal tr; 
        tr = tr[1:]
        tr.append(ti)
        tr.sort()

    def add_failure_time(ti):
        nonlocal ts; 
        ts = ts[1:]
        ts.append(ti)
        ts.sort()

    while True:
        if ts[0] < tr[0]: # Caso 1 de Ross
            t = ts[0]
            r += 1
            if r == S+1:
                return t
            if r < S+1:
                x = random.expovariate(TF)
                add_failure_time(t + x)
            if math.inf in tr:
                y = random.expovariate(TR)
                add_repair_time(t + y)
        else:
            t = tr[0]
            r = r - 1
            if r > 0:
                y = random.expovariate(TR)
                add_repair_time(t + y)
            if r == 0:
                tr = tr[1:]
                tr.append(math.inf)
                tr.sort()
                add_repair_time(math.inf)





def gen_ej1(): return sim_ross(ops=2)

n = 100_000

esp,var = lib.sim_esp_var(gen_ej1, n)
print(esp, var)

print(sum(ns))
print(ns)

    
            
