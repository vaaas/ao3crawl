#!/usr/bin/env python3

# how do ratings relate to hits, kudos, bookmarks, comments?
# how do fandoms relate to ratings?
# how do ratings relate to fandoms?
# how do different fandoms reward ratings?
# how do ratings relate to categories?

import sys
import json
import statistics
import math
import matplotlib.pyplot as plt

def space():
	sys.stdout.write("\n\n\n")

def parse(line): return json.loads(line)

def getsecond(x): return x[1]

def incrkey(dic, key, amount=1):
	dic[key] = dic[key] + amount if key in dic else amount

ratings = ["Not Rated", "General Audiences", "Teen And Up Audiences", "Mature", "Explicit"]
categories = ["F/F", "F/M", "Gen", "M/M", "Multi", "Other", "No category"]

objs = [parse(line) for line in sys.stdin]

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

for rating in ratings:
	for number in ["hits", "kudos", "bookmarks", "comments"]:
		lst = [work[number] for work in objs if work["rating"] == rating]
		mean = statistics.mean(lst)
		print("Mean %s for works rated %s: %f" %(number, rating, mean))
space()

fandomworks = dict()
for work in objs:
	if work["rating"] not in ratings: continue
	vfandoms = []
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			vfandoms.append(fandom)
	for fandom in vfandoms:
		if fandom not in fandomworks:
			fandomworks[fandom] = { rating: 0 for rating in ratings }
		fandomworks[fandom][work["rating"]] += 1

rankings = dict()
for rating in ratings:
	lst = []
	for fandom in viable_fandoms:
		lst.append((fandom, fandomworks[fandom][rating] / fandom_counter[fandom]))
	lst.sort(key=getsecond)
	rankings[rating] = lst

for rating in ratings:
	print("Top fandoms with more works rated %s, proportionately" % (rating,))
	for tup in rankings[rating][:-21:-1]:
		print("%s: %f" % tup)
	space()

fandomhits = dict()
for work in objs:
	if work["rating"] not in ratings: continue
	vfandoms = []
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			vfandoms.append(fandom)
	for fandom in vfandoms:
		if fandom not in fandomhits:
			fandomhits[fandom] = { rating: 0 for rating in ratings }
		fandomhits[fandom][work["rating"]] += work["hits"]

for fandom in fandomhits:
	for rating in fandomhits[fandom]:
		fandomhits[fandom][rating] = fandomhits[fandom][rating] / fandomworks[fandom][rating]

hranks = dict()
for rating in ratings:
	lst = []
	for fandom in viable_fandoms:
		lst.append((fandom, fandomhits[fandom][rating]))
	lst.sort(key=getsecond)
	hranks[rating] = lst

for rating in ratings:
	print("Top fandoms with more hits for works rated %s, proportionately" % (rating,))
	for tup in hranks[rating][:-21:-1]:
		print("%s: %f" % tup)
	space()

catworks = {cat: {rating: 0 for rating in ratings} for cat in categories}
catcounter = {cat: 0 for cat in categories}
for work in objs:
	for cat in work["categories"]:
		catcounter[cat] += 1
		if work["rating"] in ratings:
			catworks[cat][work["rating"]] += 1

cranks = {cat: {rating: 0 for rating in ratings} for cat in categories}
for cat in cranks:
	for rating in cranks[cat]:
		cranks[cat][rating] = catworks[cat][rating] / catcounter[cat]

for cat in cranks:
	for rating in cranks[cat]:
		print("Proportion of works rated %s in category %s: %f" % (rating, cat, cranks[cat][rating]))
	space()
