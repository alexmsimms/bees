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
    out.close()
    hive_life.close()
    plot.plot_bee_pops()
    plot.plot_hive_vitality()

    win.getMouse()
    win.close()

def eval_fitness(population):
    day = []
    for chromo in population:
        day.append(eval_individual(chromo))

    pool = [bee[0] for bee in day if int(bee[1])==0]

    nectar_brought_in = sum(pool)

    simulate(day)

    global hive_nectar
    hive_nectar -= 1 # Food to feed the queen bee?
    if hive_nectar < 10:
        hive_nectar += nectar_brought_in * .25

    hive_life.write("{}\n".format(hive_nectar))

    avg = nectar_brought_in * 0.9/len(pool) if len(pool) > 0 else 0

    if hive_nectar > 10:
        modifier = 1
    elif hive_nectar > 0:
        modifier = hive_nectar / 10
    else:
        modifier = .01 #if you give something 0 fitness,
                       #can get div by 0 errors

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

def simulate(day):

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

    time.sleep(.3)
    
    for i in range(len(bees)):
      food[i].undraw()
      if int(day[i][1])==0:
        bees[i].setFill('green')
      elif int(day[i][1])==1:
        bees[i].setFill('red')
      else:
        print day[i][1]

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
