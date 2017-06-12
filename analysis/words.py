#!/usr/bin/env python3

# how do words relate to kudos, comments, bookmarks, hits?
# how do fandoms relate to words?
# how do different fandoms reward verbosity?
# how are word counts distributed?

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

fcounter = dict()
fwords = dict()

for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fcounter, fandom)
		incrkey(fwords, fandom, work["words"])

fandom_words = dict()
for fandom in fwords:
	if fcounter[fandom] >= 100:
		fandom_words[fandom] = fwords[fandom]/fcounter[fandom]

rankings = [(fandom, fandom_words[fandom]) for fandom in fandom_words]
rankings.sort(key=getsecond, reverse=True)

print("Most verbose fandoms")
for tup in rankings[:20]:
	print("%s: %f" % tup)
space()

words = list()
hits = list()
kudos = list()
comments = list()
bookmarks = list()
hpw = list()
for work in objs:
	words.append(work["words"])
	hits.append(work["hits"])
	kudos.append(work["kudos"])
	comments.append(work["comments"])
	bookmarks.append(work["bookmarks"])
	hpw.append(work["hits"]/work["words"] if work["words"] > 0 else 0)

maxwords = max(words)


plt.scatter(words, hits)
plt.plot(words, trendfn(words,hits)(words), color="red")
plt.xlabel("Words in a work")
plt.ylabel("Hits in a work")
plt.savefig("figs/wordshitsdistribution.png")
plt.close()

plt.scatter(words,kudos)
plt.plot(words, trendfn(words,kudos)(words), color="red")
plt.xlabel("Words in a work")
plt.ylabel("Kudos in a work")
plt.savefig("figs/wordskudosdistribution.png")
plt.close()

plt.scatter(words,comments)
plt.plot(words, trendfn(words,comments)(words), color="red")
plt.xlabel("Words in a work")
plt.ylabel("Comments in a work")
plt.savefig("figs/wordscommentsdistribution.png")
plt.close()

plt.scatter(words,bookmarks)
plt.plot(words, trendfn(words,bookmarks)(words), color="red")
plt.xlabel("Words in a work")
plt.ylabel("Bookmarks in a work")
plt.savefig("figs/wordsbookmarksdistribution.png")
plt.close()

plt.scatter(words,hpw)
plt.plot(words, trendfn(words,hpw)(words), color="red")
plt.xlabel("Words in a work")
plt.ylabel("Hits per word in a work")
#plt.savefig("figs/wordsreturnsdistribution.png")
#plt.close()
plt.show()

swords = sorted(words)
length = len(swords)
thatorless = [100*i/length for i in range(length)]
plt.plot(swords, thatorless, linestyle="-")
plt.xscale("log")
plt.xlabel("Words in a work")
plt.ylabel("% at same length or less")
plt.savefig("figs/worddistribution.png")
plt.close()

mean = statistics.mean(words)
median = statistics.median(words)
mode = statistics.mode(words)
var = statistics.variance(words)
print("Mean words are: %f" % (mean,))
print("Median words are: %f" % (median,))
print("Mode words are: %f" % (mode,))
print("Word variance is: %f" % (var,))
space()

halfwords = sum(words)/2
cnt = 0
amount = 0
for entry in words[::-1]:
	amount += entry
	cnt += 1
	if amount >= halfwords:
		break
print("The top %d (%f%%) most verbose words account for half of all words." % (cnt, 100*cnt/len(words)))
space()

fandom_counter = dict()
for work in objs:
	for fandom in work["fandoms"]:
		incrkey(fandom_counter, fandom)

viable_fandoms = { fandom for fandom in fandom_counter if fandom_counter[fandom] >= 100 }

fandom_wh = dict()
for work in objs:
	for fandom in work["fandoms"]:
		if fandom in viable_fandoms:
			if not fandom in fandom_wh: fandom_wh[fandom] = list()
			fandom_wh[fandom].append((work["words"], work["hits"]))

fandom_corr = dict()
for fandom in fandom_wh:
	fandom_corr[fandom] = statistics.mean([(x[1]/x[0] if x[0] != 0 else 0) for x in fandom_wh[fandom]])

rankings = [(fandom, fandom_corr[fandom]) for fandom in fandom_corr]
rankings.sort(key=getsecond, reverse=True)
print("The fandoms which reward verbosity the most are:")
for tup in rankings[:10]:
	print("%s: %f" % tup)

