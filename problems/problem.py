# coding: utf-8
from abc import ABC, abstractmethod
# import numpy as np



class Problem(ABC):
    @abstractmethod
    def __init__(self):
        self.solvers_dict = {
            'exhaustive': self.ExhaustiveSearch,
            'greedy': self.GreedyAlg,
            'dynamic': self.Dynamic,
        }
        self.P = {} # instance of the problem
        self.data = None


    def resolve(self, method):
        return self.solvers_dict[method.lower()]()


    def ExhaustiveSearch(self):
        raise Exception('This method is not defined')


    def GreedyAlg(self):
        raise Exception('This method is not defined')


    def Dynamic(self):
        raise Exception('This method is not defined')

