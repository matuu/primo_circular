# coding: utf-8
import sys


def criba_eratostenes(n):
    """
    La criba de Eratóstenes es un algoritmo que permite hallar todos los números
    primos menores que un número natural dado N.
    """
    l = list()
    multiplos = set()
    for i in range(2, n+1):
        if i not in multiplos:
            l.append(i)
            multiplos.update(range(i*i, n+1, i))
    return l


def rotar(item):
    l = len(item)
    combinaciones = list()
    for i in range(l):
        aux = ""
        for j in range(l):
            aux += item[((i+j) % l)]
        combinaciones.append(int(aux))
    return combinaciones


def es_circular(n):
    """
    "Al número 197 se lo llama “primo circular“ porque todas las rotaciones de
    sus dígitos: 197, 971 y 719 son a su vez números primos"

    Por lo tanto, no podrán ser primos circular aquellos que contengan un digito par,
    ya que alguna rotación no será un número primo. Sucede igual con el 5 y el 0.

    Lo que nos deja en que prodrán ser "primo circular" los número compuestos por los
    digitos 1, 3, 7 y 9.

    """
    primos_circulares = list()  # guardamos los primos circulares
    primos = criba_eratostenes(n)  # busco todos lo primos menores a N
    # Por cada primo menor a n
    for item in primos:
        if item not in primos_circulares:  # si ya es un primo circular no ingreso
            # compruebo si sólo contiene los digitos 1, 3, 7 y/o 9
            if not [x for x in str(item) if x not in ["1", "3", "7", "9"]]:
                # compruebo cada rotación de sus digitos
                num_rot = list()  # lista con primos con digitos rotados
                comb = rotar(str(item))
                for rot in comb:
                    if rot in primos:
                        num_rot.append(rot)
                if len(str(item)) == len(num_rot):  # si la cantidad de digitos es igual a las combinaciones de primos
                    primos_circulares.extend(num_rot)  # añado todos los primos circulares

    # ordeno y quito repetidos
    resultado = sorted(set(primos_circulares))
    return resultado


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Uso: primo_cir.py [natural_num]"
        exit()
    if not str(sys.argv[1]).isdigit():
        print u"El primer argumento debe ser un número"
        print "Uso: primo_cir.py [natural_num]"
        exit()

    print es_circular(int(sys.argv[1]))
