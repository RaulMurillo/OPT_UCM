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
        self.costs = np.array([i[0] for i in self.data])
        # data[:,0] is number of elements in set
        print()
        print("="*10+" The Set Covering Problem "+"="*10)
        print("* Number of sets:", N_sets)
        print("* Number of elements:", N_elems)
        # print("* DATA:", self.data) # Caution when using large data
        print('-'*42)
        print()

    def get_cost(self, subset):
        return sum(e for s in subset for e in s[:1])

    
    def resolve(self, method):
        print("Solving Set cover Problem using " + method + " algorithm")
        (best_price, best_sets) = super().resolve(method)
        if len(best_sets):
            print("Best solution, with price %d takes sets:" %
                (best_price))
            # best_sets.sort()
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
            cost = self.get_cost(picked_sets)
            covered_elems = set(e for s in picked_sets for e in s[1:]) # Covered elements[1:]

            if covered_elems == U:
                # print('covered_elems!  cost:', cost, best_price)
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


    def Genetic(self):
        N_individuals = 20
        N_iters = 15
        U = set(range(1, self.P['N_elems']+1)) # Universe of elements

        best_price = -1
        best_sets = []

        def fitness(indiv, U):
            covered_elems = get_elems(indiv)
            fit = int(covered_elems == U)
            # picked_sets = list(itertools.compress(self.data, indiv))
            # print("picked_sets:",picked_sets)
            cost = sum(self.costs[indiv])
            # cost = self.get_cost(picked_sets)
            return fit/cost

        def get_elems(indiv):
            picked_sets = list(itertools.compress(self.data, indiv))
            return set(e for s in picked_sets for e in s[1:]) # Covered elements

        # Create initial random population
        population = (np.random.rand(N_individuals, self.P['N_sets']) > 0.5)
        pop_fitness = np.empty(2*N_individuals)

        for _ in range(N_iters):
            print('population:', population)
            # Alteration
            np.random.shuffle(population)
            new_population = (np.empty_like(population)).tolist()

            # Cross population by (random) pairs
            for k in range(len(population)//2):
                cut = np.random.randint(0, self.P['N_sets']+1)
                print(k, cut)
                new_population[2*k] = np.concatenate([population[2*k][:cut], population[2*k + 1][cut:]])
                new_population[2*k + 1] = np.concatenate([population[2*k][cut:], population[2*k + 1][:cut]])
            print('new_population:', new_population)
            
            tmp_pop = np.concatenate([population, new_population])
            print('tmp_pop:\n', tmp_pop)
            # Compute fitness
            for j, indiv in enumerate(tmp_pop):
                covered_elems = get_elems(indiv)
                f = fitness(indiv, U)
                pop_fitness[j] = f

            # Sort by fitness
            indices = np.argsort(pop_fitness)
            print('pop_fitness:', pop_fitness)
            print('indices:', indices)
            

            # Selection
            population = tmp_pop[indices[N_individuals:]]
            best_sets = tmp_pop[indices[-1]]

        # best_picked_sets = list(itertools.compress(self.data, best_sets))
        best_price = sum(self.costs[best_sets]) # self.get_cost(best_picked_sets)
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


    my_Set = read_file('data/set_cover_10.txt')
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
    my_SetCover.resolve('genetic') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')