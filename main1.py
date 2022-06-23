import random
import itertools
import matplotlib.pyplot as plt
import numpy as np
from Net import Network, Connection


# used for the traffic matrix
def main():
    sat_percent = 95
    # fixed rate_____________________________________________________________________________
    network = Network('247000.json')
    n_node = len(network.nodes.keys())
    saturationFix = []
    MsFix = []
    M = 1
    while 1:
        t_mtx = np.ones((n_node, n_node)) * 100 * M
        for i in range(n_node):
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network.nodes.keys(), 2))
        n_elem = len(elements)
        for e in elements:  # remove the diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(100):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network.upgrade_traffic_matrix(t_mtx, el[0], el[1])
            if (val == 0) | (val == np.inf):
                elements.remove(el)
        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                    sat += 1
        sat = sat / n_elem * 100
        saturationFix.append(sat)
        MsFix.append(M)
        if sat > sat_percent:
            break
        M += 1
        network.free_space()
    plt.plot(MsFix, saturationFix)
    plt.title('Saturation Fixed-Rate')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.show()

main()