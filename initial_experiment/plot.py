from matplotlib.pyplot import *
import numpy


def plot_a_thing():
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
	# xlabel("Transaction time (epoch)")
	# ylabel("Exchange Rate (USD)")
	show()
