# Ejercicio 1

## Contexto
- El ejercicio plantea que tenemos N cajas funcionando y S repuestos.
- Tenemos también que un reparador arregla las cajas en cierto tiempo.
- Se quiere ver cuál es el tiempo promedio en el que hayan S + 1 cajas fuera de funcionamiento(nos quedamos sin repuestos)

## Observaciones
- En cada momento dado, el tiempo esperado en el que fallará otra caja es $\frac{1}{N*T_F}$
- En cada momento dado, el tiempo esperado en el que el taller arreglá una caja es $\frac{1}{N*T_R}$
- Una vez que hay una caja en el taller, hay dos eventos posibles: se arregla antes una caja o bien se rompe antes otra. La probabilidad del primero es $\frac{T_R}{T_F N + T_R}$ y la del segundo es $\frac{T_R}{T_F N + T_R}$.

Entonces podemos simular nuestra situación de la siguiente manera:

```python
TF = ... # tasa de fallo
TR = ... # tasa de reparacion
N = ...  # cantidad de cajas
S = ...  # cantidad de repuestos
B = 0    # cantidad de cajas rotas
t = 0    # tiempo transcurrido

alpha = TR/(TF*N + TR) # probabilidad de arreglar antes de que se rompa otra

while True:
    if B == 0: # mecanico sin trabajar
        # Solo puede romperse una maquina, simulamos el tiempo y lo sumamos:

        t += simexp(1/(N*TF))
        B += 1
        if B == S:
            break
    else: # mecanico tiene al menos una maquina rota esperando
        # Pueden pasar dos cosas: una maquina se arregla u otra se rompe

        u = random()

        if u <= alpha: # se arregla una antes de que se rompa otra
            t += simexp(1/TR)
            B -= 1
        else:          # se rompe otra antes de arreglar
            t += simexp(1/(TF*N))

            B += 1
            if B == S:
                break



```
