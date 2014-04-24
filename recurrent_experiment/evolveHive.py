from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import random
import plot
from bee import Bee
import cPickle as pickle
out = open("log.csv", 'w')
hive_life = open("hive.csv", 'w')
hive_nectar = 10.0
week_length = 7
to_pickle = []


def main():
    config.load('NEATconfig')
    chromosome.node_gene_type = genome.NodeGene

    population.Population.evaluate = eval_fitness
    generations = 100
    pop = population.Population()
    pop.epoch(generations, report=True, save_best=True,
              checkpoint_interval=None, checkpoint_generation=5)
    out.close()
    hive_life.close()
    pickle.dump(to_pickle, open("pickle.p", "wb"))
    plot.plot_bee_pops()
    plot.plot_hive_vitality()

def eval_fitness(population):
    generation = []
    hive = [Bee(chromo) for chromo in population]
    for day in xrange(week_length):
        one_day(hive)
    for i in xrange(len(population)):
        generation.append(hive[i].choices())
        population[i].fitness = hive[i].avg_fitness()
    to_pickle.append(generation)

def one_day(hive):
    global hive_nectar

    for bee in hive:
        bee.evaluate(hive_nectar)
    pool = [bee.found_nectar() for bee in hive if bee.was_altruistic()]

    nectar_brought_in = sum(pool)

    hive_nectar -= 1 # Food to feed the queen bee?
    if hive_nectar < 10:
        hive_nectar += nectar_brought_in * .25

    hive_life.write("{}\n".format(hive_nectar))

    avg = nectar_brought_in * 0.9/len(pool) if len(pool) > 0 else 0

    # modifier = 1
    if hive_nectar > 10:
        modifier = 1
    elif hive_nectar > 5:
        modifier = hive_nectar /10
    else:
        modifier = .001 
                   #if you give something 0 fitness,
                   #can get div by 0 errors

    altruistic = 0
    selfish = 0

    for bee in hive:
        if bee.was_altruistic():
            bee.set_fitness(avg * modifier)
            altruistic+=1
        else:
            bee.set_fitness(bee.found_nectar() * modifier)  #/2
            selfish+=1
    out.write("{},{}\n".format(altruistic, selfish))


if __name__ == '__main__':
    main()
