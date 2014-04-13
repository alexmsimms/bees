from matplotlib.pyplot import *
import numpy


def plot_bee_pops():
	altruistic = []
	selfish = []


	with open("log.csv") as file:
	    data = file.read()
	    for line in data.split():
	        altruistic.append(float(line.split(',')[0]))
	        selfish.append(float(line.split(',')[1]))

	time = range(len(altruistic))
	plot(time, altruistic)
	plot(time, selfish)

	legend(("Altruistic Bees?", "Selfish Bees?"))

	show()


def plot_hive_vitality():
	with open("hive.csv") as f:
		hive_vitality = map(float, f.read().split())
	time = range(len(hive_vitality))

	plot(time, hive_vitality)
	axhline(color='r')
	show()


if __name__ == '__main__':
	plot_bee_pops()
	plot_hive_vitality()