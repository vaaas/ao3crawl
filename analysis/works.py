#!/usr/bin/env python3
# which are the most common fandoms?
# how are they distributed?

import sys
import json
import statistics
import math
import matplotlib.pyplot as plt

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

length = len(wcsort)
total = 0
for i in wcsort: total += i[1]
print("The total is %d" % (total,))
space()

print("The amount of fandoms is %d" % (length,))
space()

print("The top 20 fandoms are:")
for i in wcsort[:20]: print("%s - %d occurrences (%f%%)" % (i[0], i[1], 100*i[1]/total))
count = 0
for i in range(20):
	count += wcsort[i][1]
print("Together, they occur %d times" % (count,))
print("This is %f%% of total" % (100*count/total,))
space()

for i in (1,5,10,20,33,50):
	endpoint = int((length / 100) * i)
	count = 0
	for j in range(endpoint):
		count += wcsort[j][1]
	print("The top %d%% of fandoms have %d occurrences" % (i, count))
	print("This is %f%% of total" % (100*count/total,))
	space()

target = int(total / 2)
count = 0
num = 0
for i in wcsort:
	count += i[1]
	num += 1
	if count >= target: break
print("%d fandoms account for 50%% of the effect" % (num,))
print("These are %f%% of fandoms" % (100*num/length,))
space()

for i in (1,2,3,4,5,6,7,8,9,10,100,1000):
	n = 0
	for (fandom, count) in wcsort[::-1]:
		if count > i: break
		else: n += 1
	print("%d (%f%%) fandoms appear %d times or less" % (n, 100*n/length, i))
space()

mean = statistics.mean(map(getsecond, wcsort))
print("The mean is: %f" % (mean,))
median = statistics.median(map(getsecond, wcsort))
print("The median is: %f" % (median,))
mode = statistics.mode(map(getsecond, wcsort))
print("The mode is: %d" % (mode,))
pvar = statistics.variance(map(getsecond, wcsort), mean)
print("The variance is: %f" % (pvar,))
print("The standard deviation is: %f" % (math.sqrt(pvar),))

plotnumsd = dict()
for fandom in wcsort:
	incrkey(plotnumsd, fandom[1])
amountworks = sorted(list(plotnumsd.keys()))
percenttotal = [100*plotnumsd[i]/length for i in amountworks]
for i in range(len(percenttotal)-1,0,-1):
	percenttotal[i] = sum(percenttotal[:i+1])
percenttotal[-1] = 100

plt.plot(amountworks, percenttotal, linestyle="-")
plt.xscale("log")
plt.xlabel("Fandom appears X times or less")
plt.ylabel("% of fandoms")
plt.savefig("figs/worksfandomsdistribution.png")
