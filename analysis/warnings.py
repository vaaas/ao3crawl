#!/usr/bin/env python3
# what we want to do
# how do warnings relate to hits, kudos, comments, bookmarks?
# which fandoms warn more?

import sys
import json
import statistics
import math
import matplotlib.pyplot as plt
from scipy.stats import pearsonr as corr

def space():
	sys.stdout.write("\n\n\n")

def parse(line): return json.loads(line)

def getsecond(x): return x[1]

def incrkey(dic, key, amount=1):
	dic[key] = dic[key] + amount if key in dic else amount

def myline(x, multiplier=1, addition=0):
	return multiplier*x + addition

objs = [parse(line) for line in sys.stdin]

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

warnums = dict()
fandomwarns = dict()

for work in objs:
	for warning in work["warnings"]:
		if warning not in warnums: warnums[warning] = list()
		warnums[warning].append({"hits": work["hits"], "kudos": work["kudos"], "bookmarks": work["bookmarks"], "comments": work["comments"]})

for warning in warnums:
	for thing in ["hits", "kudos", "bookmarks", "comments"]:
		stuff = [x[thing] for x in warnums[warning]]
		mean = statistics.mean(stuff)
		median = statistics.median(stuff)
		mode = statistics.mode(stuff)
		print("Mean %s for works warned %s is: %f" %(thing, warning, mean))
		print("Median %s for works warned %s is: %f" %(thing, warning, median))
		print("Mode %s for works warned %s is: %f" %(thing, warning, mode))
		space()

fcount = dict()
for work in objs:
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			if not fandom in fcount: fcount[fandom] = dict()
			for warning in work["warnings"]:
				incrkey(fcount[fandom], warning)

for warning in warnums:
	rankings = [(fandom, fcount[fandom][warning]/fandom_counter[fandom]) for fandom in fcount if warning in fcount[fandom]]
	rankings.sort(key=getsecond, reverse=True)
	print("The fandoms which warned the most for %s on average are:" %(warning,))
	for tup in rankings[:20]:
		print("%s: %f" % tup)
	space()
