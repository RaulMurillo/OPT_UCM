#!/usr/bin/env python
# coding: utf-8
import numpy as np
import csv
import random

N = 20
W_max = 100

Weigths =  np.random.randint(0, 60, size=N) #random.sample(range(0, 20), N)
Values  =  np.random.randint(0, 50, size=N)

Mochila = np.row_stack(([N, W_max], np.column_stack((Weigths, Values))))

# print(Mochila)

with open('data/mochila.csv', 'w', newline='') as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    wr.writerows(Mochila)

