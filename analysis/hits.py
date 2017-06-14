#!/usr/bin/env python3

# hit to kudo, bookmark, comment ratio
# fandoms with higher rates of hits
# how are hits distributed?

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

def trendfn(x,y):
	return numpy.poly1d(numpy.polyfit(x,y,1))

objs = [parse(line) for line in sys.stdin]

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

hits = []
kudos = []
bookmarks = []
comments = []

fhits = dict()
for work in objs:
	hits.append(work["hits"])
	kudos.append(work["kudos"])
	bookmarks.append(work["bookmarks"])
	comments.append(work["comments"])

	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			incrkey(fhits, fandom, work["hits"])

for fandom in fhits:
	fhits[fandom] = fhits[fandom] / fandom_counter[fandom]

mean = statistics.mean(hits)
median = statistics.median(hits)
mode = statistics.mode(hits)
print("Mean hits are: %f" % (mean,))
print("Median hits are: %f" % (median,))
print("Mode hits are: %f" % (mode,))
space()

ranking = [(fandom, fhits[fandom]) for fandom in fhits]
ranking.sort(key=getsecond, reverse=True)
print("Average hits for works in fandoms")
for tup in ranking[:20]:
	print("%s: %f" % tup)
space()

hit2kudo = [(kudos[i]/hits[i] if hits[i] != 0 else 0) for i in range(len(hits))]
hit2bookmark = [(bookmarks[i]/hits[i] if hits[i] != 0 else 0) for i in range(len(hits))]
hit2comment = [(comments[i]/hits[i] if hits[i] != 0 else 0) for i in range(len(hits))]

mean = statistics.mean(hit2kudo)
median = statistics.median(hit2kudo)
print("Mean kudos per hit are: %f" % (mean,))
print("Median kudos per hit are: %f" % (median,))

mean = statistics.mean(hit2bookmark)
median = statistics.median(hit2bookmark)
print("Mean bookmark per hit are: %f" % (mean,))
print("Median bookmark per hit are: %f" % (median,))

mean = statistics.mean(hit2comment)
median = statistics.median(hit2comment)
print("Mean comment per hit are: %f" % (mean,))
print("Median comment per hit are: %f" % (median,))
space()

plt.scatter(hits, kudos)
plt.plot(hits, trendfn(hits, kudos)(hits), color="red")
plt.xlabel("Hits in a work")
plt.ylabel("Kudos in a work")
plt.savefig("figs/hitskudosdistribution.png")
plt.close()

plt.scatter(hits, bookmarks)
plt.plot(hits, trendfn(hits, bookmarks)(hits), color="red")
plt.xlabel("Hits in a work")
plt.ylabel("Bookmarks in a work")
plt.savefig("figs/hitsbookmarksdistribution.png")
plt.close()

plt.scatter(hits, comments)
plt.plot(hits, trendfn(hits, comments)(hits), color="red")
plt.xlabel("Hits in a work")
plt.ylabel("Comments in a work")
plt.savefig("figs/hitscommentsdistribution.png")
plt.close()
