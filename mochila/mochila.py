#!/usr/bin/env python
# coding: utf-8
import csv
import numpy as np
import itertools


with open('data/mochila.csv', 'r', newline='') as csv_file:
    Mochila = list(csv.reader(csv_file))
    
# Convert ot int
Mochila = np.array(Mochila, dtype=int)
# print(Mochila)

N = Mochila[0][0]
W_max = Mochila[0][1]
Mochila = Mochila[1:]
assert len(Mochila)==N
print()
print("="*10+" The Knapsack Problem "+"="*10)
print("* Number of elements:", N)
print("* Maximum weight allowed:", W_max)
print('-'*40)
print()

max_val = 0
max_w = 0
best = []

for mask in itertools.product([True, False], repeat=N):
    # print(Mochila[mask,:])
    selection = np.sum(Mochila[mask,:], axis=0)
    # print(selection[0])

    if selection[0] <= W_max:
        if selection[1] > max_val:
            max_val = selection[1]
            max_w = selection[0]
            best = mask

print("Best solution has weight %d and value %d" %(max_w, max_val))
print(best)
