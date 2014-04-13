#!/usr/bin/python
import sys
import os

path = sys.argv[1]
os.mkdir(path)
os.system("mv *chromo* {}/".format(path))
os.system("mv check* {}/".format(path))
os.system("mv log.csv {}/".format(path))
os.system("mv hive.csv {}/".format(path))
os.system("cp evolveHive.py {}/".format(path))
os.system("cp NEATconfig {}/".format(path))