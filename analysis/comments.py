#!/usr/bin/env python3

# which fandoms comment the most?
# how are comments distributed?

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

objs = [parse(line) for line in sys.stdin]

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

comments = [work["comments"] for work in objs]

mean = statistics.mean(comments)
median = statistics.median(comments)
mode = statistics.mode(comments)
var = statistics.variance(comments)
print("Mean comments are: %f" % (mean,))
print("Median comments are: %f" % (median,))
print("Mode comments are: %f" % (mode,))
print("Comment variance is: %f" % (var,))
space()

halfcomments = sum(comments)/2
cnt = 0
amount = 0
for entry in comments[::-1]:
	amount += entry
	cnt += 1
	if amount >= halfcomments:
		break
print("The top %d (%f%%) most commented works account for half of all comments." % (cnt, 100*cnt/len(comments)))
space()

scomms = sorted(comments)
length = len(scomms)
thatorless = [100*i/length for i in range(length)]
plt.plot(scomms, thatorless, linestyle="-")
plt.xscale("log")
plt.xlabel("Comments in a work")
plt.ylabel("% at same amount or less")
plt.savefig("figs/commentdistribution.png")
plt.close()

fcomms = dict()
for work in objs:
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			if not fandom in fcomms: fcomms[fandom] = 0
			fcomms[fandom] += work["comments"]

rankings = [(fandom, fcomms[fandom] / fandom_counter[fandom]) for fandom in fcomms]
rankings.sort(key=getsecond, reverse=True)
print("The fandoms which comment the most on average are:")
for tup in rankings[:10]:
	print("%s: %f" % tup)
