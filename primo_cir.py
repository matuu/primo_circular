#!/usr/bin/python2
# coding: utf-8
import sys
import threading
import Queue


"""
"Al número 197 se lo llama “primo circular“ porque todas las rotaciones de
sus dígitos: 197, 971 y 719 son a su vez números primos"

Por lo tanto, no podrán ser primos circular aquellos que contengan un digito par,
ya que alguna rotación no será un número primo. Sucede igual con el 5 y el 0.

Lo que nos deja en que prodrán ser "primo circular" los número compuestos por los
digitos 1, 3, 7 y 9.

"""


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


class Worker(threading.Thread):
    def __init__ (self, l_primos, q):
        self.l_primos = l_primos
        self.q = q
        threading.Thread.__init__ (self)

    def run(self):
        # se ejecuta en un hilo separado
        self.encontrar_primos_circular(self.l_primos)

    def rotar(self, item):
        """
        Método que devuelve una lista números que son el resultado de rotar los
        dígitos del número dado.
        """
        l = len(item)
        combinaciones = list()
        for i in range(l):
            aux = ""
            for j in range(l):
                aux += item[((i+j) % l)]
            combinaciones.append(int(aux))
        return combinaciones

    def encontrar_primos_circular(self, primos):
        p_circulares = list()
        for item in primos:
            if item not in p_circulares:  # si ya es un primo circular no ingreso
                # compruebo si sólo contiene los digitos 1, 3, 7 y/o 9
                if not [x for x in str(item) if x not in ["1", "3", "7", "9"]]:
                    # compruebo cada rotación de sus digitos
                    num_rot = list()  # lista con primos con digitos rotados
                    comb = self.rotar(str(item))
                    for rot in comb:
                        if rot in primos:
                            num_rot.append(rot)
                    if len(str(item)) == len(num_rot):  # si la cantidad de digitos es igual a las combinaciones de primos
                        p_circulares.extend(num_rot)  # añado todos los primos circulares

        # ordeno y quito repetidos
        resultado = sorted(set(p_circulares))
        self.q.put(resultado)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Uso: primo_cir.py [num_natural]"
        exit()
    if not str(sys.argv[1]).isdigit():
        print u"El primer argumento debe ser un número"
        print "Uso: primo_cir.py [num_natural]"
        exit()
    n = int(sys.argv[1])
    if n <= 0:
        print u"[num_natural] debe ser un número natural mayor a 0"
        exit()

    primos_circulares = Queue.Queue()  # pila de primos circulares

    primos = criba_eratostenes(n)  # busco todos los primos menores a n
    c_thread = len(str(n))  # cantidad de digitos del número n

    threads = []
    # un hilo por cada subconjunto de primos, determinado por su número de
    # digitos
    for i in range(c_thread):
        l_primos = [x for x in primos if len(str(x)) == (i + 1)]
        if l_primos:
            t = Worker(l_primos, primos_circulares)
            threads.append(t)
            t.setDaemon(True)

    # arranco todos los hilos
    [x.start() for x in threads]
    # espero a que todos finalicen
    [x.join() for x in threads]

    # muestro los resultados
    result = []
    while not primos_circulares.empty():
        result.extend(primos_circulares.get())
    print result
