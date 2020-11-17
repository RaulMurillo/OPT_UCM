from problem import Problem
import numpy as np
import itertools
import csv


class Knapsack(Problem):
    def __init__(self, N, max_W, data):
        super().__init__()
        self.P = {"N": N, 'max_W': max_W}
        self.data = data
        # data[:,0] are profits
        # data[:,1] are weights
        print()
        print("="*10+" The Knapsack Problem "+"="*10)
        print("* Number of elements:", N)
        print("* Maximum weight allowed:", max_W)
        print('-'*42)
        print()

    def resolve(self, method):
        print("Solving Knapsack Problem using " + method + " algorithm ...")
        (best_profit, best_w, best_set) = super().resolve(method)
        print("Best solution, with weight %d and profit %d, takes elements:" %
              (best_w, best_profit))
        print(best_set)
        print("%d elements in total\n" %(len(best_set)))

    def ExhaustiveSearch(self):
        best_profit = 0
        best_w = 0
        best_set = []

        for mask in itertools.product([True, False], repeat=self.P['N']):
            selection = np.sum(self.data[mask, ], axis=0)

            if selection[1] <= self.P['max_W']:
                if selection[0] > best_profit:
                    best_profit = selection[0]
                    best_w = selection[1]
                    best_set = mask

        return (best_profit, best_w, best_set)

    def GreedyAlg(self):
        best_profit = 0
        best_w = 0
        best_set = []

        # density = profit/weight
        density = self.data[:, 0]/self.data[:, 1]
        # Use [::-1] to get descending order
        ordered_d = np.argsort(density, kind='quicksort')[::-1]

        for obj in ordered_d:
            if best_w + self.data[obj, 1] <= self.P['max_W']:
                best_profit += self.data[obj, 0]
                best_w += self.data[obj, 1]
                best_set.append(obj)

        return (best_profit, best_w, best_set)


    def Dynamic(self, _profit=None):
        # Profit oriented - http://didawiki.cli.di.unipi.it/lib/exe/fetch.php/magistraleinformatica/ad/ad_17/vazirani_knapsack.pdf
        if _profit is None:
            profit = self.data[:,0]
        else:
            # The profits are given as input
            profit = _profit
        # Add base/corner case - No object is taken
        profit = np.append(0, profit)
        weight = np.append(0, self.data[:,1])
        
        P = np.sum(profit) # This is faster and smaller than `P = N*max_profit`, as original Vazirani's text propose
        # print(P) # Number of columns in the matrix

        # first row of weights-matrix `M`, all infinity except column with profit equal as first object's profit
        M = (np.zeros((self.P['N']+1, P+1), dtype=np.uint64)-1).astype(np.uint64)
        M[0, profit[0]] = weight[0]
        for i in range(1, self.P['N']+1):
            for j in range(P+1):
                if profit[i] > j: # profit(obj_i) > j
                    M[i,j] = M[i-1, j]
                else:
                    M[i,j] = min(M[i-1, j], weight[i]+M[i-1, j-profit[i]])

        # Get maximum profit & weight
        valid_pos = (np.argwhere(M[-1, :] <= self.P['max_W']))
        best_profit = np.max(valid_pos)
        best_w = M[-1, best_profit]

        # Get the optimal set of objects
        current_p = best_profit
        current_w = best_w
        best_set = []
        for r in range(self.P['N']+1, -1, -1):
            if M[r-1, current_p] == current_w:
                # object-r is not taken
                continue
            else:
                assert(M[r, current_p] == M[r-1, current_p-profit[r]] + weight[r])
                # object r-1 is taken, but it is in position r
                best_set.insert(0, r-1)
                current_p -= profit[r]
                current_w -= weight[r]
        
        return (best_profit, best_w, best_set)

    def FPTAS(self):
        eps = 0.1
        P = np.max(self.data[:,0])
        K = eps * P / self.P['N']

        # Compute new profits
        profit = np.floor_divide(self.data[:,0], K).astype(int)

        # Apply dynamic algorithm with new profits
        _, best_w, best_set = self.Dynamic(profit)
        # best_profit is not given by dynamic algorithm, since profits where modified
        best_profit = np.sum(self.data[best_set, 0])
        return (best_profit, best_w, best_set)



def read_file(fname):
    with open(fname, 'r', newline='') as csv_file:
        data = list(csv.reader(csv_file, delimiter=' '))
    # Convert to int
    return np.array(data, dtype=int)


if __name__ == "__main__":
    # import numpy as np
    import time


    Mochila = read_file('data/knapsack.csv')
    N = Mochila[0][0]
    max_W = Mochila[0][1]
    Mochila = Mochila[1:]

    my_mochila = Knapsack(N, max_W, Mochila)
    tic = time.time()
    my_mochila.resolve('fptas') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    