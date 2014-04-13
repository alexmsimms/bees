from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import random
import plot

out = open("log.csv", 'w')

def main():
    config.load('NEATconfig')
    chromosome.node_gene_type = genome.NodeGene

    population.Population.evaluate = eval_fitness
    generations = 500
    pop = population.Population()
    pop.epoch(generations, report=True, save_best=True,
              checkpoint_interval=None, checkpoint_generation=5)
    out.close()
    plot.plot_a_thing()

def eval_fitness(population):
    day = []
    for chromo in population:
        day.append(eval_individual(chromo))
    pool = [bee[0] for bee in day if int(bee[1])==0]

    avg = sum(pool)/len(pool) if len(pool) > 0 else 0

    altruistic = 0
    selfish = 0

    for chromo, production in zip(population, day):
        if int(production[1]) == 0:
            chromo.fitness = avg
            altruistic+=1
        else:
            chromo.fitness = production[0]
            selfish+=1
    out.write("{},{}\n".format(altruistic, selfish))

def eval_individual(chromo):
    brain = nn.create_phenotype(chromo)
    found_nectar = random.random()

    brain.flush()
    output = brain.sactivate([found_nectar])

    return (found_nectar, output[0])

if __name__ == '__main__':
    main()