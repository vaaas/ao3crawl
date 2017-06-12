#!/usr/bin/env python3

# hit to kudo, bookmark, comment ratio
# fandoms with higher hits
# fandoms with higher rates of hits
# how are hits distributed?

import sys
import json
import statistics
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def space():
	sys.stdout.write("\n\n\n")

def parse(line):
	return json.loads(line)

def incrkey(dic, key):
	dic[key] = dic[key] + 1 if key in dic else 1

def getsecond(x): return x[1]

objs = map(parse, sys.stdin)

workcount = dict()
for work in objs:
	if work["fandoms"] == None: incrkey(workcount, None)
	else:
		for fandom in work["fandoms"]: incrkey(workcount, fandom)

wcsort = sorted(workcount.items(), key=getsecond, reverse=True)
