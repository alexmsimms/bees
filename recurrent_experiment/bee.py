from neat.nn import nn_pure as nn
import random
class Bee(object):
    def __init__(self, chromo):
        self.chromo = chromo
        self.inputs    = [()]
        self.outputs   = [(0,)]
        self.fitnesses = [.5]

    def was_selfish(self):
        return self.outputs[-1] <= 0

    def was_altruistic(self):
        return self.outputs[-1] > 0

    def found_nectar(self):
        return self.outputs[-1][0]

    def set_fitness(self, fitness):
        self.fitnesses.append(fitness)

    def avg_fitness(self):
        choice_fitnesses = self.fitnesses[1:]
        return sum(choice_fitnesses) / len(choice_fitnesses)

    def evaluate(self, hive_nectar):
        brain = nn.create_phenotype(self.chromo)
        found_nectar = random.random()
        print self.outputs
        ins = (found_nectar, 
               self.outputs[-1][0], 
               self.fitnesses[-1], 
               hive_nectar)
        brain.flush()
        outs = brain.sactivate(ins)
        self.inputs.append(ins)     
        self.outputs.append(outs)
        
