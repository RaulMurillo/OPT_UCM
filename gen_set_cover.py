#!/usr/bin/env python
# coding: utf-8
import csv
import random
from pathlib import Path
Path("data").mkdir(parents=True, exist_ok=True)

def gen_elems(N_elems):
    # There is no posibility any set contains all elements
    n = random.randint(1, N_elems-1) # 1 <= n <= N_elems-1  # uniform distribution
    randomlist = random.sample(range(1, N_elems+1), n) # Take n random unique elements (without replacement)
    randomlist.sort()
    return randomlist

def gen_sets(N_sets, N_elems, max_cost=10, sep=' ', filename='set_cover'):
    """Function that generates a file of integer tuples for using as input for 
    set cover problems.

    For each tuple, the first element indicates the cost, which is in the 
    range [1, `max_cost`], and the rest of elements inficates the elements
    of the set, which are between 1 and `N_elems`.

    There is a total of `N_sets`+1 tuples, or rows written in the file, 
    where each row stands for a different set, and the first-one indicates
    the problem conditions, namely, `N_sets`, `N_elems`.

    The resulting file has the format:  
    N_sets N_elems  
    cost_1 e_11 e12 ...  
    cost_2 e_21 e22 ...  
    ...  
    cost_n e_n1 en2 ...  

    Parameters
    ----------
    N_sets : int
        The number of sets/tuples.
    N_elems : int
        The problem restriction (e.g. the total number of elements to cover).
    max_cost : int, optional
        The maximum cost for each set. Default is 10.
    """
    data = [[N_sets, N_elems]]

    U = set(range(1, N_elems+1))
    avail_elems = set()

    while True:
        for s in range(N_sets):
            cost = random.randint(1, max_cost)
            elems = gen_elems(N_elems)
            avail_elems.update(elems)
            elems.insert(0,cost)
            data.append(elems)
        # Assert all elements are contained in universe of sets
        if U.issubset(avail_elems):
            break
        # Reset data
        avail_elems.clear()
        data = [[N_sets, N_elems]]

    with open('data/'+filename+'_'+str(N_sets)+'.txt', 'w', newline='') as csv_file:
        wr = csv.writer(csv_file, delimiter=sep)
        wr.writerows(data)


if __name__ == "__main__":

    gen_sets(15, 1000, max_cost=100)
