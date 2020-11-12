from problem import Problem
import numpy as np
import itertools
import csv


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
        print("* DATA:", self.data)
        print('-'*42)
        print()
    
    def resolve(self, method):
        print("Solving Set cover Problem using " + method + " algorithm")
        (best_price, best_sets) = super().resolve(method)
        print("Best solution, with price %d takes sets:" %
              (best_price))
        print(best_sets)
        print()

    def GreedyAlg(self):
        best_price = 0
        best_sets = []

        # U = np.arange(self.P['N_elems']) # Universe of elements
        # C = np.empty() # Covered elements
        U = set(range(1, self.P['N_elems']+1))
        C = set()

        price = np.empty(self.P['N_sets'], dtype=float)

        k = 0
        # while not all(elem in covered for elem in universe):
        while C != U:
            print('sets are:', C, U)
            # Find the set whose cost-effectiveness is smallest
            for i, S_set in enumerate(self.data):
                # print(i)
                S_cost = int(S_set[0])
                S = set(S_set[1:])
                diff = len(S.difference(C))
                print(S)
                print(diff)
                if diff:
                    price[i] = S_cost / diff
                else: # avoid 0 division error
                    price[i] = np.inf
                    # TODO: Remove set from list
                print(price[i])
            S_ind = np.argmin(price)#, kind='quicksort')

            # Pick such set
            best_price += int(self.data[S_ind][0])
            S = self.data[S_ind][1:]
            best_sets.append(S_ind)

            #########
            print('Choosing set',S_ind, 'with elems', S)

            # C <- C Union S
            C = C.union(S)
            print(C)

            print('+'*15)
            
            #########
            k+=1
            if k > 3:
                exit(1)

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


    my_Set = read_file('data/set_cover.csv')
    N_sets = int(my_Set[0][0])
    N_elems = int(my_Set[0][1])
    data = my_Set[1:]


    my_SetCover = Set_Covering(N_sets, N_elems, data)
    # print(my_Set)
    # exit(0)
    tic = time.time()
    my_SetCover.resolve('greedy') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)