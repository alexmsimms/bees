from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import random
import plot
from bee import Bee
out = open("log.csv", 'w')
hive_life = open("hive.csv", 'w')
share = open("share.csv", 'w')
exp = open("neg.txt", 'w')
hive_nectar = 10.0
majority = .5
week_length = 7

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
    share.close()
    plot.plot_bee_pops()
    plot.plot_guidance()
    plot.plot_hive_vitality()

def eval_fitness(population):
    hive = [Bee(chromo) for chromo in population]
    for day in xrange(week_length):
        one_day(hive)
    for i in xrange(len(population)):
        population[i].fitness = hive[i].avg_fitness()

def get_directions(bee):
  if bee.outputs[-1][1] >= .5 and bee.inputs[-1][0] > .5:
    return bee.inputs[-1][0]
  else:
    return 0

def one_day(hive):

    directions = 0

    global hive_nectar
    global majority    
    for b in range(len(hive)):
        guidance = get_directions(hive[b-1])
        hive[b].evaluate(hive_nectar, majority, guidance)
        directions+=1 if guidance > 0 else 0

    share.write("{}\n".format(directions))
        
          

    #majority calculation
    majority = sum([bee.was_altruistic() for bee in hive])/len(hive)

    pool = []
    
    '''
    for bee in hive:
      if bee.was_selfish():
        pool.append(bee.found_nectar()+(bee.found_nectar()*bee.outputs[-1][0]))
      else:
        pool.append(bee.found_nectar())
    '''

    pool = [bee.found_nectar() for bee in hive if bee.was_altruistic()]

    nectar_brought_in = sum(pool)

    hive_nectar -= 1 # Food to feed the queen bee?
    if hive_nectar < 10:
        hive_nectar += nectar_brought_in * .25

    hive_life.write("{}\n".format(hive_nectar))

    avg = nectar_brought_in * 0.9/len(pool) if len(pool) > 0 else 0

    if hive_nectar > 10:
        modifier = 1
    elif hive_nectar > 0:
        modifier = hive_nectar /10
    else:
        modifier = .0000000000000000001 
                   #if you give something 0 fitness,
                   #can get div by 0 errors

    altruistic = 0
    selfish = 0

    for bee in hive:
        if bee.was_altruistic():
            bee.set_fitness(avg * modifier) #adjust for hive fitness or not
            altruistic+=1
        else:
            #food = -1*(bee.found_nectar()*bee.outputs[-1][0])
            food = bee.found_nectar()
            bee.set_fitness(food * modifier)  #/2
            selfish+=1
    out.write("{},{}\n".format(altruistic, selfish))

def eval_individual(chromo, last_choice, last_fitness, hive_nectar):
    brain = nn.create_phenotype(chromo)
    found_nectar = random.random()

    brain.flush()
    output = brain.sactivate([found_nectar, last_choice, last_fitness, hive_nectar])
    exp.write(str(output[0])+'\n')
    return (found_nectar, output[0])


if __name__ == '__main__':
    main()
