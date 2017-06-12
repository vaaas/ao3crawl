#!/usr/bin/env python3

# how does chapter amount relate to kudos, hits, bookmarks. comments?
# distribution of chapters

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

chapters = list()
hits = list()
kudos = list()
comments = list()
bookmarks = list()

for work in objs:
	chapters.append(work["chapters"])
	hits.append(work["hits"])
	kudos.append(work["kudos"])
	comments.append(work["comments"])
	bookmarks.append(work["bookmarks"])

maxchapters = max(chapters)

cor = corr(chapters,hits)
plt.scatter(chapters, hits)
plt.plot([0,maxchapters], [0 + cor[1], maxchapters*cor[0] + cor[1]], color="red")
plt.xlabel("Chapters in a work")
plt.ylabel("Hits in a work")
plt.savefig("figs/chaptershitsdistribution.png")
plt.close()

cor = corr(chapters,kudos)
plt.scatter(chapters, kudos)
plt.plot([0,maxchapters], [0 + cor[1], maxchapters*cor[0] + cor[1]], color="red")
plt.xlabel("Chapters in a work")
plt.ylabel("kudos in a work")
plt.savefig("figs/chapterskudosdistribution.png")
plt.close()

cor = corr(chapters,comments)
plt.scatter(chapters, comments)
plt.plot([0,maxchapters], [0 + cor[1], maxchapters*cor[0] + cor[1]], color="red")
plt.xlabel("Chapters in a work")
plt.ylabel("comments in a work")
plt.savefig("figs/chapterscommentsdistribution.png")
plt.close()

cor = corr(chapters,bookmarks)
plt.scatter(chapters, bookmarks)
plt.plot([0,maxchapters], [0 + cor[1], maxchapters*cor[0] + cor[1]], color="red")
plt.xlabel("Chapters in a work")
plt.ylabel("bookmarks in a work")
plt.savefig("figs/chaptersbookmarksdistribution.png")
plt.close()

schaps = sorted(chapters)
length = len(schaps)
thatorless = [100*i/length for i in range(length)]

haveone = 100*len([True for work in objs if work["chapters"] == 1]) / len(objs)

mean = statistics.mean(schaps)
median = statistics.median(schaps)
mode = statistics.mode(schaps)
var = statistics.variance(schaps)
print("Mean chapters are: %f" % (mean,))
print("Median chapters are: %f" % (median,))
print("Mode chapters are: %f" % (mode,))
print("chapter variance is: %f" % (var,))
print("%f%% of works have 1 chapter" % (haveone,))

plt.plot(schaps, thatorless, linestyle="-")
plt.xscale("log")
plt.xlabel("Chapters in a work")
plt.ylabel("% at same or fewer")
plt.savefig("figs/chaptersdistribution.png")
