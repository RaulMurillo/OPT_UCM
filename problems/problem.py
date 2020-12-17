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
            'fptas': self.FPTAS,
            'genetic': self.Genetic,
        }
        self.P = {} # instance of the problem
        self.data = None


    def resolve(self, method, **kwargs):
        return self.solvers_dict[method.lower()](**kwargs)


    def ExhaustiveSearch(self):
        raise Exception('This method is not defined')


    def GreedyAlg(self):
        raise Exception('This method is not defined')


    def Dynamic(self):
        raise Exception('This method is not defined')


    def FPTAS(self):
        raise Exception('This method is not defined')


    def Genetic(self, **kwargs):
        raise Exception('This method is not defined')
    

