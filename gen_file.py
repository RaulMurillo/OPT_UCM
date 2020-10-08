#!/usr/bin/env python
# coding: utf-8
import numpy as np
import csv

def gen_tuples(n, c, obj_w=30, obj_v=30, sep=' ', filename='tuple_'):
    """Function that generates a file of tuples for using as input for 
    multiple problems.

    The tuples are integers in range ([1, `obj_v`], [1, `obj_w`] ) with random 
    uniform distribution.

    The first tuple consists on (`n`, `c`).

    The resulting file has the format:  
    n   c  
    v_1 w_1  
    v_2 w_2  
    ...  
    v_n w_n  

    Parameters
    ----------
    n : int
        The number of tuples.
    c : int
        The problem restriction (e.g. the knapsack capacity).
    obj_w: int, optional
        Maximum weight of each object.
    obj_v: int, optional
        Maximum value of each object.
    """
    Values = np.random.randint(obj_v, size=n) + 1
    Weigths = np.random.randint(obj_w, size=n) + 1
    # assert np.min(Weigths)==1
    # assert np.max(Weigths)==obj_w
    r = np.row_stack(([n, c], np.column_stack((Values, Weigths))))

    with open('data/'+filename+str(n)+'.csv', 'w', newline='') as csv_file:
        wr = csv.writer(csv_file, delimiter=sep)
        wr.writerows(r)


if __name__ == "__main__":
    gen_tuples(10, 100, 30, 30, filename='mochila_heavy_')
    gen_tuples(15, 100, 30, 30, filename='mochila_heavy_')
    gen_tuples(20, 100, 30, 30, filename='mochila_heavy_')

    gen_tuples(10, 100, 10, 30, filename='mochila_light_')
    gen_tuples(15, 100, 10, 30, filename='mochila_light_')
    gen_tuples(20, 100, 10, 30, filename='mochila_light_')
