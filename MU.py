# Programa que obtiene una probabilidad de obtener una cadena menor o igual que 2
# al generar teoremas del sistema formal MIU (Hofstadter)

import numpy as np
import random
import pandas as pd

################################## FUNCIONES DE APOYO

# 1) MxI -> MxU
def addu(string):
    #print("MxI -> MxU")
    if string[-1] == 'I':
        return string + 'U'
    return string

## 2) Mx -> Mxx
def duplicate(string):
    #print("Mx -> Mxx")
    return string + string[1:]

## 3) MxIIIx -> MxUx
def iforu(string):
    #print("MxIIIx -> MxUx")
    return string.replace('III', 'U')


## 4) MxUUx -> Mxx
def ufornot(string):
    #print("MxUUx -> Mxx")
    return string.replace('UU', '')

## Generar reglas aleatoriamente
def apply_rule(string):
    cad = ''
    rule = random.randint(1, 4)
    if string != 'MU':
        if rule == 1:
            cad = addu(string)
        elif rule == 2:
            cad = duplicate(string)
        elif rule == 3:
            cad = iforu(string)
        elif rule == 4:
            cad = ufornot(string)
    else:
        cad = string
    return cad

## Para cada iteracion genera Muestra numero de cadenas, a las cuales aplica cierto numero de reglas
def iterate(string, Muestra = 100, reglas = 5):
    count   = 0
    lengths = []
    while count < Muestra:
        stemp = string
        p = 0
        while p < reglas:
            stemp = apply_rule(stemp)
            p = p + 1
        count  = count + 1
        lengths.append(len(stemp))
    return lengths

## Promedio de longitud de cada una de las iteraciones
def mean_dist(string, iteraciones = 1000, Muestra = 1000, reglas = 5):
    means = []
    for i in range(iteraciones):
        lengths = iterate(string, Muestra=Muestra, reglas=reglas)
        means.append(np.mean(lengths))
    return means

################################## PROGRAMA
resultado = []
df=pd.DataFrame()
i = 0
lim_95 = 0
while(True):
    #en cada iteracion se obtienen 100 promedios, cada uno a partir de 1000 cadenas, con 5 reglas aplicadas
    n_promedios = 100
    promedios = mean_dist("MI", iteraciones=n_promedios, Muestra=1000, reglas=5)

    mean = sum(promedios)/len(promedios)
    std = np.sqrt(sum([np.power((m-mean),2) for m in promedios])/len(promedios))

    #obtener rangos de deciles
    Q=10
    rango = [[-5.0,-1.2815],
             [-1.2815, -0.8416],
             [-0.8416, -0.5243],
             [-0.5243, -0.2532],
             [-0.2532, 0.0],
             [0.0, 0.2532],
             [0.2532, 0.5243],
             [0.5243, 0.8416],
             [0.8416, 1.2815],
             [1.2815, 5.0]]

    #cada punto restar media y dividir entre desviacion estandar, resulta: media 0, desviacion estandar 1
    estandarizada = [(x-mean)/std for x in promedios]

    o = [] #observado
    for r in rango:
        olen = len([x for x in estandarizada if x > r[0] and x <= r[1]])
        o.append(olen)

    esperado = len(estandarizada)/Q

    estadistico_L = sum([np.power(o[i]-esperado,2)/esperado for i in range(Q)])
    resultado.append([o, estadistico_L])

    print("Iteracion: {}, Estadistico_L: {}".format(i, estadistico_L))
    i=i+1

    # It may be seen that for all the range (50 < n < 100) a value of 3.2 guarantees that the
    # observations are Gaussian with a probability of, at least, 0.95
    if(estadistico_L < 3.2):
        print("Es Normal con media: {}, Desviacion estándar: {}".format(mean, std))

        # chevichev P(μ-mσ ≤ c ≤ μ+m σ)>1-1/m^2
        lim_95 = mean-np.sqrt(20)*std
        print("Por Chevichev podemos inferir que el 95% de las cadenas son mayores que {}".format(lim_95))

        # combinar datos en dataframe para grafica
        df = pd.DataFrame.from_items([('long_prom', promedios), ('tipo', str(i) + "_" + str(estadistico_L))])
        break

## Histogram
#p = ggplot(df, aes(x='long_prom', color='tipo'))
#p + geom_density()
#p + geom_vline(xintercept = lim_95)
#p.show()
