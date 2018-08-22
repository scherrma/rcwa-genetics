from copy import deepcopy
from numpy.random import choice
from random import random

class Generation:
    def __init__(self, size, seed, mutation_rate = 0.1, elite = 1):
        self.pop = [seed] + [seed.mutate() for i in range(size - 1)]
        self.elite, self.muta_rate = elite, mutation_rate
        self.best = None

    def __str__(self):
        return '\n'.join(map(str, self.pop))

    def evaluate(self, progress_txt = None):
        for i in range(len(self.pop)):
            self.pop[i].evaluate()
            if progress_txt is not None:
                print(progress_txt, " ", i, "/", len(self.pop), sep = '', end = '\r')
        if progress_txt is not None:
            print(progress_txt, ' ' * (2*len(str(len(self.pop))) + 1), end = '\r')

        self.pop.sort(key = lambda x: x.fom, reverse=True)
        self.best = self.pop[0]

    def progeny(self):
        self.evaluate()
        totalfitness = sum([x.fom for x in self.pop])
        fitnesses = [g.fom/totalfitness for g in self.pop]

        children = deepcopy(self)
        children.pop = self.pop[:self.elite]
        for i in range(len(self.pop) - self.elite):
            parents = choice(self.pop, 2, False, fitnesses)
            child = parents[0].crossbreed(parents[1])
            if random() < self.muta_rate:
                child = child.mutate()
            children.pop.append(child)
        return children
