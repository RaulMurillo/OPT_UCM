from problem import Problem
import numpy as np
import itertools
import csv
import sys


class Set_Covering(Problem):
    def __init__(self, N_sets, N_elems, data):
        super().__init__()
        # self.solver = solvers_dict[solver.lower()]()
        self.P = {"N_sets": N_sets, 'N_elems': N_elems}
        self.data = data
        # data[:,0] is number of elements in set
        print()
        print("="*10+" The Set Covering Problem "+"="*10)
        print("* Number of sets:", N_sets)
        print("* Number of elements:", N_elems)
        # print("* DATA:", self.data) # Caution when using large data
        print('-'*42)
        print()
    
    def resolve(self, method):
        print("Solving Set cover Problem using " + method + " algorithm")
        (best_price, best_sets) = super().resolve(method)
        if len(best_sets):
            print("Best solution, with price %d takes sets:" %
                (best_price))
            best_sets.sort()
            print(best_sets)
        else:
            print('<< ERROR: This instance of set cover has no solution! >>')
        print()

    def ExhaustiveSearch(self):
        best_price = sys.maxsize
        best_sets = []
        m = None

        U = set(range(1, self.P['N_elems']+1)) # Universe of elements

        elements = set(e for s in self.data for e in s[1:])
        # Check the subsets cover the universe
        if elements != U:
            return (best_price, best_sets)

        for mask in itertools.product([True, False], repeat=self.P['N_sets']):
            picked_sets = list(itertools.compress(self.data, mask))
            cost = sum(e for s in picked_sets for e in s[:1])
            covered = set(e for s in picked_sets for e in s[1:]) # Covered elements

            if covered == U:
                # print('covered!  cost:', cost, best_price)
                if cost < best_price:
                    best_price = cost
                    best_sets = mask

        best_sets = list(itertools.compress(range(self.P['N_sets']), best_sets))
        return (best_price, best_sets)




    def GreedyAlg(self):

        best_price = 0
        best_sets = []

        U = set(range(1, self.P['N_elems']+1)) # Universe of elements
        C = set() # Covered elements

        elements = set(e for s in self.data for e in s[1:])
        # Check the subsets cover the universe
        if elements != U:
            return (best_price, best_sets)


        price = np.empty(self.P['N_sets'], dtype=float)

        # while not all(elem in covered for elem in universe):
        while C != U:
            # Find the set whose cost-effectiveness is smallest
            for i, S_set in enumerate(self.data):
                S_cost = int(S_set[0])
                S = set(S_set[1:])
                diff = len(S.difference(C))
                # print(S)
                # print(diff)
                if diff:
                    price[i] = S_cost / diff
                else: # avoid 0 division error
                    price[i] = np.inf
                    # TODO: Remove set from list might speed-up the algorithm
                # print(price[i])
            S_ind = np.argmin(price)

            # Pick such set
            best_price += int(self.data[S_ind][0])
            S = self.data[S_ind][1:]
            best_sets.append(S_ind)
            # print('Choosing set',S_ind, 'with elems', S)

            # C <- C Union S
            C = C.union(S)

        return (best_price, best_sets)



def read_file(fname):
    with open(fname, 'r', newline='') as csv_file:
        data = list(csv.reader(csv_file, delimiter=' '))

    # Convert to int
    data = [[int(j) for j in i] for i in data]
    return data


if __name__ == "__main__":
    # import numpy as np
    import time


    my_Set = read_file('data/set_cover_15.txt')
    N_sets = int(my_Set[0][0])
    N_elems = int(my_Set[0][1])
    data = my_Set[1:]


    my_SetCover = Set_Covering(N_sets, N_elems, data)
    
    tic = time.time()
    my_SetCover.resolve('greedy') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')
    
    tic = time.time()
    my_SetCover.resolve('exhaustive') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')