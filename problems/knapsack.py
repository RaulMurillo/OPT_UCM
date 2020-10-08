from problem import Problem
import numpy as np
import itertools


class Knapsack(Problem):
    def __init__(self, N, max_W, data):
        super().__init__()
        # self.solver = solvers_dict[solver.lower()]()
        self.P = {"N": N, 'max_W': max_W}
        self.data = data
        print()
        print("="*10+" The Knapsack Problem "+"="*10)
        print("* Number of elements:", N)
        print("* Maximum weight allowed:", max_W)
        print('-'*42)
        print()

    def resolve(self, method):
        print("Solving Knapsack Problem using " + method + " algorithm")
        (max_val, max_w, best) = super().resolve(method)
        print("Best solution, with weight %d and value %d, takes elements:" %
              (max_w, max_val))
        print(best)
        print(np.arange(self.P["N"])[np.array(best)])
        print()

    def ExhaustiveSearch(self):
        max_val = 0
        max_w = 0
        best = []

        for mask in itertools.product([True, False], repeat=self.P['N']):
            # print(Mochila[mask,:])
            selection = np.sum(self.data[mask, ], axis=0)
            # print(selection[0])

            if selection[1] <= self.P['max_W']:
                if selection[0] > max_val:
                    max_val = selection[0]
                    max_w = selection[1]
                    best = mask

        return (max_val, max_w, best)

    def GreedyAlg(self):
        max_val = 0
        max_w = 0
        best = []

        # density = value/weight
        density = self.data[:, 0]/self.data[:, 1]
        # Use [::-1] to get descending order
        ordered_d = np.argsort(density, kind='quicksort')[::-1]

        for obj in ordered_d:
            if max_w + self.data[obj, 1] <= self.P['max_W']:
                max_val += self.data[obj, 0]
                max_w += self.data[obj, 1]
                best.append(obj)

        return (max_val, max_w, best)


def read_file(fname):
    with open(fname, 'r', newline='') as csv_file:
        data = list(csv.reader(csv_file, delimiter=' '))
    # Convert to int
    return np.array(data, dtype=int)


if __name__ == "__main__":
    import csv
    import numpy as np
    import time

    ########
    Mochila = read_file('data/mochila_heavy_10.csv')
    N = Mochila[0][0]
    max_W = Mochila[0][1]
    Mochila = Mochila[1:]

    my_mochila = Knapsack(N, max_W, Mochila)
    tic = time.time()
    my_mochila.resolve('exhaustive')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))
    tic = time.time()
    my_mochila.resolve('greedy')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))

    ########
    Mochila = read_file('data/mochila_heavy_15.csv')
    N = Mochila[0][0]
    max_W = Mochila[0][1]
    Mochila = Mochila[1:]

    my_mochila = Knapsack(N, max_W, Mochila)
    tic = time.time()
    my_mochila.resolve('exhaustive')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))
    tic = time.time()
    my_mochila.resolve('greedy')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))

    ########
    Mochila = read_file('data/mochila_heavy_20.csv')
    N = Mochila[0][0]
    max_W = Mochila[0][1]
    Mochila = Mochila[1:]

    my_mochila = Knapsack(N, max_W, Mochila)
    tic = time.time()
    my_mochila.resolve('exhaustive')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))
    tic = time.time()
    my_mochila.resolve('greedy')
    toc = time.time()
    print("Elapsed time: %g\n" % (toc-tic))
