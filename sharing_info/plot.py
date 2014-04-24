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

	#axvline(x=15, color = 'r')
	#axvline(x=34, color = 'r')

	# title("Prediction vs Reality for The Mt.Gox Crash")
	# title("Prediction vs Reality for BTC-e Prices")
	legend(("Altruistic Bees?", "Selfish Bees?"))
	xlabel("Generation")
	ylabel("Population")
	show()

def plot_guidance():
        directions = []

        with open("share.csv") as f:
            data = f.read()
            for line in data.split():
              directions.append(float(line))

        time = range(len(directions))
        plot(time, directions)

        #axhline(color='r')
        xlabel("Generation")
        ylabel("Population")
        show()

def plot_hive_vitality():
	with open("hive.csv") as f:
		hive_vitality = map(float, f.read().split())
	time = range(len(hive_vitality))

	plot(time, hive_vitality)
	axhline(color='r')
	xlabel("Generation")
	ylabel("Nectar Reserves")
	show()


if __name__ == '__main__':
	plot_bee_pops()
        plot_guidance()
	plot_hive_vitality()
