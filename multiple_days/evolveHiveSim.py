from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
from graphics import *
import random
import plot

out = open("log.csv", 'w')
hive_life = open("hive.csv", 'w')
hive_nectar = 10.0
win = GraphWin('Hive',500,500)



def main():

    hive = Rectangle(Point(240,240),Point(260,260))
    hive.setFill('orange')
    hive.draw(win)

    config.load('NEATconfig')
    chromosome.node_gene_type = genome.NodeGene

    population.Population.evaluate = eval_fitness
    generations = 50
    pop = population.Population()
    pop.epoch(generations, report=True, save_best=True,
              checkpoint_interval=None, checkpoint_generation=5)
    
    global win
    win.getMouse()
    win.close()
    
    out.close()
    hive_life.close()
    #plot.plot_bee_pops()
    #plot.plot_hive_vitality()

    
def eval_fitness(population):

    #last_decision = []
    #last_majority = []
    #last_nectar = []

    #for i in range(len(population)):  #initialize last nectar array
    #  last_nectar[i] = 0.5

    days = []

    altruistic = 0
    selfish = 0

 
    for i in range(3):
        days.append = eval_trial(population)
    
    for trial in days:
      #day by day

      for i in range(len(trial)):
        #bee by bee

        hive_nectar = trial[i][0][1]
        if hive_nectar > 10:
            modifier = 1
        elif hive_nectar > 0:
            modifier = hive_nectar / 10
        else:
            modifier = .01 #if you give something 0 fitness,
                       #can get div by 0 error


        if trial[i][1] < 0:
            sumfood[i] = avg * modifier
            altruistic+=1
        else:
            sumfood[i] = trial[i][0][0] * modifier
            selfish+=1

    for i in range(len(population)):
        population[i].fitness = sumfood[i]/3

    """
    for chromo, production in zip(population, days):
        if production[1] < 0:
            chromo.fitness = avg * modifier
            altruistic+=1
        else:
            chromo.fitness = production[0] * modifier
            selfish+=1
    """
    out.write("{},{}\n".format(altruistic, selfish))

      
def eval_trial(population):
    day = []
    global hive_nectar
    for chromo in population:
        day.append(eval_individual(chromo, hive_nectar)) #add input

    pool = [bee[0] for bee in day if int(bee[1])==0]

    nectar_brought_in = sum(pool)

    simulate(day)

    global hive_nectar
    hive_nectar -= 1 # Food to feed the queen bee?
    if hive_nectar < 10:
        hive_nectar += nectar_brought_in * .25

    hive_life.write("{}\n".format(hive_nectar))

    avg = nectar_brought_in * 0.9/len(pool) if len(pool) > 0 else 0

    return day


def eval_individual(chromo, hive_nectar):
    brain = nn.create_phenotype(chromo)
    found_nectar = random.random()

    brain.flush()
    output = brain.sactivate([found_nectar, hive_nectar]) #add input

    return ([found_nectar, hive_nectar], output[0]) 
    #return tuple of inputs and outputs

def simulate(day):
    global win
    bees = []  
    food = []
    for result in day:

      bx = 250
      by = 250
      bee = Circle(Point(bx,by),5)
      bee.setFill('black')
      bees.append(bee)

      nx = random.randrange(500)
      ny = random.randrange(500)
      nectar = Circle(Point(nx,ny),result[0]*20)
      nectar.setFill('yellow')
      food.append(nectar)

      bee.draw(win)
      nectar.draw(win)

    
    for i in range(15):
      for j in range(len(bees)):
        nx = food[j].getCenter().getX()
        ny = food[j].getCenter().getY()
        bees[j].move((nx-250)/15, (ny-250)/15)
        time.sleep(.001)

    time.sleep(.1)
    
    for i in range(len(bees)):
      food[i].undraw()
      if day[i][1] < 0:
        bees[i].setFill('green')
      else:
        bees[i].setFill('red')

    time.sleep(.2)

    for i in range(15):
      for j in range(len(bees)):
        nx = food[j].getCenter().getX()
        ny = food[j].getCenter().getY()
        bees[j].move((250-nx)/15,(250-ny)/15)
        time.sleep(.001)

    for i in bees:
      i.undraw()



if __name__ == '__main__':
    main()
