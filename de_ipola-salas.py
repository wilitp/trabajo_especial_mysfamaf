import lib
import math
import random

import time
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


# ===================== TESTS =====================
n = 10_000
# --------------------- TIME ---------------------
def timed(sim, show=False):
    times = [] 
    # CUIDADO CON EL RANGO DEL LOOP, entre 50 y 100 tarda minutos
    for _ in range(10): 
        t0 = time.perf_counter()
        esp,var = lib.sim_esp_var(sim, n)
        t = time.perf_counter()
        times.append(t-t0)
    avg = sum(times)/len(times)
    if show: print(f"esp {esp:.4f}, runtime {avg:.4f}")
    return avg

# --------------------- Faliure time ---------------------
def proposed_solutions_test(sim, show=False):
    
    def extra_worker(): return(sim(ops=2))
    def extra_machine():return(sim(S=4))
    def default():      return(sim())
    
    esp1,var1 = lib.sim_esp_var(extra_worker, n)
    esp2,var2 = lib.sim_esp_var(extra_machine, n)
    esp3,var3 = lib.sim_esp_var(default, n)
    
    if show: print(f"actual {esp3:.4f}, ops+1 {esp1:.4f}, S+1 {esp2:.4f}")
    return esp1, esp2, esp3
 
# ===================== METRICS =====================


def bar_plot_expected_fail_time():
    
    esp_extra_worker, esp_extra_machine, esp_def = \
        proposed_solutions_test(solucion_alternativa_1)
    
    data = {
        "Sistema Original": esp_def,
        "Extra Operario": esp_extra_worker,
        "Extra Maquina": esp_extra_machine
    }

    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color=["#ffe28a","#fb2e01","#6fcb9f"])

    plt.title('Tiempo esperado de fallas')
    plt.ylabel('Tiempo promedio (meses)')

    plt.savefig('comparacion_mejoras.png')
      
def bar_plot_expected_fail_time_5workers():
    
    def original():return solucion_alternativa_1()
    def extra_workers():return solucion_alternativa_1(ops=5)
    
    esp_def, _ = lib.sim_esp_var(original, n)
    esp_extra_worker, _ = lib.sim_esp_var(extra_workers, n)
    
    data = {
        "Sistema Original": esp_def,
        "Sistema con 5 Operarios": esp_extra_worker,
    }

    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color=["#ffe28a","#fb2e01"])

    plt.title('Tiempo esperado con distinta cantidad de operarios')
    plt.ylabel('Tiempo promedio (meses)')

    plt.savefig('comparacion_original_extra_op.png')  

def bar_plot_performance():
    # Recomendado para los tiempos cambiar la linea 115 
    
    t1 = timed(solucion_alternativa_1)
    t2 = timed(solucion_alternativa_2)
    t3 = timed(solucion_sugerida)
    
    data = {
        "Algoritmo sugerido por la catedra": t3,
        "Algoritmo alternativo 1":t1,
        "Algoritmo alternativo 2":t2,
    }

    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))    
    plt.bar(categories, values, color=["#ffe28a","#fb2e01","#6fcb9f"])


    plt.title('Diferencia de rendimiento (tiempo) entre diferentes implementaciones')
    plt.ylabel('Tiempo promedio (segundos)')
    
    plt.savefig('comparacion_tiempos.png')  

if __name__ == "__main__":
    # t1 = timed(solucion_alternativa_1   ,True)
    # t2 = timed(solucion_alternativa_2   ,True)
    # t3 = timed(solucion_sugerida        ,True)
    
    esp_extra_worker, esp_extra_machine, esp_def = \
        proposed_solutions_test(solucion_alternativa_1,True)
    # proposed_solutions_test(solucion_alternativa_2,True)
    # proposed_solutions_test(solucion_sugerida,True)
    
    
    print(f"mejora ops++ {esp_extra_worker/esp_def :.4f},\
        mejora S++ {esp_extra_machine/esp_def:.4f}")
    

    # bar_plot_expected_fail_time()
    # bar_plot_expected_fail_time_5workers()
    # bar_plot_performance()
    pass