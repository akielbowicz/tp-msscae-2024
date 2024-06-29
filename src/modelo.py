# Definimos las dinamicas
def dinamica_1(aumento, peso_arista, inflacion=0.0, alpha=1.0):
    aumento_vecino = aumento * peso_arista
    return aumento_vecino

def dinamica_2(aumento, peso_arista, inflacion, alpha=1.0):
    aumento_vecino = inflacion
    return aumento_vecino
    
def dinamica_3(aumento, peso_arista, inflacion, alpha):
    aumento_vecino = (alpha * inflacion) + ((1 - alpha) * ((aumento) * peso_arista))
    return aumento_vecino


## Defino como se calcula la inflacion
def calcular_inflacion(precios_periodo_actual, precios_periodo_pasado):
    # Asumimos una inflación no ponderada
    # donde la "canasta" sea un producto de cada sector. Entonces,
    # la canasata es la sumatoria de los precios de todos los sectores, y con eso calculamos IPC e inflación.
    # calculo los precios actuales

    ipc_actual = sum(precios_periodo_actual) / len(precios_periodo_actual)
    ipc_pasado = sum(precios_periodo_pasado) / len(precios_periodo_pasado)
    inflacion = ((ipc_actual / ipc_pasado) - 1)  * 100
    return inflacion
