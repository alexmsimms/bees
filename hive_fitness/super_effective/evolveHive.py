from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import random
import plot

out = open("log.csv", 'w')
hive_life = open("hive.csv", 'w')
hive_nectar = 10.0


def main():
    config.load('NEATconfig')
    chromosome.node_gene_type = genome.NodeGene

    population.Population.evaluate = eval_fitness
    generations = 200
    pop = population.Population()
    pop.epoch(generations, report=True, save_best=True,
              checkpoint_interval=None, checkpoint_generation=5)
    out.close()
    plot.plot_bee_pops()
    plot.plot_hive_vitality()

def eval_fitness(population):
    day = []
    for chromo in population:
        day.append(eval_individual(chromo))

    pool = [bee[0] for bee in day if int(bee[1])==0]

    nectar_brought_in = sum(pool)

    global hive_nectar
    hive_nectar -= 1 # Food to feed the queen bee?
    hive_nectar += nectar_brought_in * .25

    hive_life.write("{}\n".format(hive_nectar))

    avg = nectar_brought_in * 0.9/len(pool) if len(pool) > 0 else 0

    modifier = hive_nectar / 10 if hive_nectar > 0 else 0

    altruistic = 0
    selfish = 0

    for chromo, production in zip(population, day):
        if int(production[1]) == 0:
            chromo.fitness = avg * modifier
            altruistic+=1
        else:
            chromo.fitness = production[0] * modifier
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