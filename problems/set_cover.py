from problem import Problem
import numpy as np
from random import shuffle
import itertools
import csv
import sys
import logging


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

    
    def resolve(self, method, **kwargs):
        print("Solving Set cover Problem using " + method + " algorithm")
        (best_price, best_sets) = super().resolve(method, **kwargs)
        if len(best_sets):
            print("Best solution, with price %d takes sets:" %
                (best_price))
            # best_sets.sort()
            if isinstance(best_sets[0], bool):
                print(list(itertools.compress(range(self.P['N_sets']), best_sets)))
                print(sum(best_sets))
            else:
                print(best_sets)
                print(len(best_sets))
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

        # best_sets = list(itertools.compress(range(self.P['N_sets']), best_sets))
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


    def Genetic(self, **kwargs):
        N_individuals = kwargs.get('N_individuals') # 10
        N_iters       = kwargs.get('N_iters') # 100
        mutation_prob = kwargs.get('mutation_prob') # 0.01
        # assert isinstance(N_individuals, int)
        # assert isinstance(N_iters, int)
        # assert isinstance(mutation_prob, float)

        U = set(range(1, self.P['N_elems']+1)) # Universe of elements

        best_price = -1
        best_sets = []

        def get_elems(indiv):
            picked_sets = list(itertools.compress(self.data, indiv))
            return set(e for s in picked_sets for e in s[1:]) # Covered elements

        def fitness(indiv, U):
            covered_elems = get_elems(indiv)
            fit = (covered_elems == U)
            # picked_sets = list(itertools.compress(self.data, indiv))
            # print("picked_sets:",picked_sets)
            cost = sum(self.costs[indiv])
            # cost = self.get_cost(picked_sets)
            if fit:
                return 1/cost
            else:
                if cost > 0:
                    return len(U - covered_elems)*(-1) + 1/cost
                else:
                    return len(U - covered_elems)*(-1)
            # return fit/cost

        class Individual:
            self.set_list = [False] * self.P['N_sets']
            self.fitness = 0.0

            def __init__(self, set_list):
                self.set_list = set_list
                self.fitness = fitness(set_list, U)

        # Create initial random population
        population = [None] * N_individuals
        children   = [None] * N_individuals

        for i in range(N_individuals):
            population[i] = Individual((np.random.rand(self.P['N_sets']) > 0.5).tolist())

        # Apply N iterations on population
        for n in range(N_iters):
            # Cross population by (random) pairs
            shuffle(population)
            for k in range(len(population)//2):
                cut = np.random.randint(1, self.P['N_sets'])
                logging.debug('Merging following 2 individuals by cuting at {}:\n{}\n{}'.format(cut,
                                            population[2*k].set_list, population[2*k+1].set_list))

                new_1 = population[2*k].set_list[:cut] + population[2*k+1].set_list[cut:]
                new_2 = population[2*k+1].set_list[:cut] + population[2*k].set_list[cut:]
                logging.debug('New individuals are::\n{}\n{}'.format(new_1, new_2))

                # Mutation on new individuals
                for indiv in [new_1, new_2]:
                    for gen in range(self.P['N_sets']): # == len(indiv)
                        if mutation_prob > np.random.rand():
                            indiv[gen] = not(indiv[gen])
                logging.debug('Mutated-New individuals are::\n{}\n{}'.format(new_1, new_2))
                
                children[2*k] = Individual(new_1)
                children[2*k + 1] = Individual(new_2)
            
            # Sort total population by fitness
            tmp_pop = population + children
            tmp_pop.sort(key=lambda x: x.fitness)
            
            # Selection of next generation - elitism method
            population = tmp_pop[-N_individuals:]
            best_sets = tmp_pop[-1].set_list
            logging.info('Iteration {} - Best fitness value: {}'.format(n+1, tmp_pop[-1].fitness))

        best_price = sum(self.costs[best_sets])
        return (best_price, best_sets)



def read_file(fname):
    with open(fname, 'r', newline='') as csv_file:
        data = list(csv.reader(csv_file, delimiter=' '))

    # Convert to int
    data = [[int(j) for j in i] for i in data]
    return data


if __name__ == "__main__":
    import time
    # logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    my_Set = read_file('data/set_cover_100.txt')
    N_sets = int(my_Set[0][0])
    N_elems = int(my_Set[0][1])
    data = my_Set[1:]


    my_SetCover = Set_Covering(N_sets, N_elems, data)
    
    tic = time.time()
    my_SetCover.resolve('greedy') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')
    #####################
    N_individuals = 10
    N_iters = 100
    mutation_prob = 0.01
    tic = time.time()
    my_SetCover.resolve('genetic', N_individuals=N_individuals, N_iters=N_iters, mutation_prob=mutation_prob) # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')