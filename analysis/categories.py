#!/usr/bin/env python3
# how do categories relate to hits, kudos, bookmarks, comments?
# how do fandoms relate to categories?

import sys
import json
import statistics
import math
import matplotlib.pyplot as plt
import numpy

def space():
	sys.stdout.write("\n\n\n")

def parse(line): return json.loads(line)

def getsecond(x): return x[1]

def incrkey(dic, key, amount=1):
	dic[key] = dic[key] + amount if key in dic else amount

objs = [parse(line) for line in sys.stdin]

categories = ["F/F", "F/M", "Gen", "M/M", "Multi", "Other", "No category"]

stats = {c: list() for c in categories}

for work in objs:
	for category in work["categories"]:
		if not category in categories: continue
		stats[category].append({"hits": work["hits"], "kudos": work["kudos"], "bookmarks": work["bookmarks"], "comments": work["comments"]})

for category in stats:
	print("Total works in category %s is: %d" %(category, len(stats[category])))
	for thing in ["hits", "kudos", "bookmarks", "comments"]:
		stuff = [x[thing] for x in stats[category]]
		mean = statistics.mean(stuff)
		median = statistics.median(stuff)
		mode = statistics.mode(stuff)
		print("Mean %s for works in category %s is: %f" %(thing, category, mean))
		print("Median %s for works in category %s is: %f" %(thing, category, median))
		print("Mode %s for works in category %s is: %f" %(thing, category, mode))
		space()

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

fcount = dict()
for work in objs:
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			if not fandom in fcount: fcount[fandom] = dict()
			for category in work["categories"]:
				incrkey(fcount[fandom], category)

for category in categories:
	rankings = [(fandom, fcount[fandom][category]/fandom_counter[fandom]) for fandom in fcount if category in fcount[fandom]]
	rankings.sort(key=getsecond, reverse=True)
	print("The fandoms which used the category %s the most on average are:" %(category,))
	for tup in rankings[:20]:
		print("%s: %f" % tup)
	space()
