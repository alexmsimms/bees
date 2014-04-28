from neat.nn import nn_pure as nn
import random
class Bee(object):
    def __init__(self, chromo):
        self.chromo = chromo
        self.inputs    = [(.5,)]
        self.outputs   = [(.5,.5)]
        self.fitnesses = [.5]

    def was_selfish(self):
        return self.outputs[-1][0] < .5

    def was_altruistic(self):
        return self.outputs[-1][0] >= .5

    def found_nectar(self):
        return self.inputs[-1][0]

    def set_fitness(self, fitness):
        self.fitnesses.append(fitness)

    def avg_fitness(self):
        choice_fitnesses = self.fitnesses[1:]
        return sum(choice_fitnesses) / len(choice_fitnesses)

    def evaluate(self, hive_nectar, majority, guidance):
        if hive_nectar > 10:
            adjusted_nectar = 1
        elif hive_nectar < 0:
            adjusted_nectar = 0
        else:
            adjusted_nectar = hive_nectar / 10

        brain = nn.create_phenotype(self.chromo)
        
        # implementing the ability for bees to be 'guided'
        if guidance:
               found_nectar = guidance
        else:
               found_nectar = random.random()
        #################################################
        
        ins = (found_nectar, 
               self.outputs[-1][0], 
               self.fitnesses[-1], 
               hive_nectar,
               majority)
               #self.inputs[-1][0])
        brain.flush()
        outs = brain.pactivate(ins)
        self.inputs.append(ins)     
        self.outputs.append(outs)
        
