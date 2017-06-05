#!/usr/bin/env python3
import sys
import os
import json

fandoms = dict()

for line in sys.stdin:
	obj = json.loads(line)
	for fandom in obj["fandoms"]:
		if fandom in fandoms:
			fandoms[fandom] += 1
		else:
			fandoms[fandom] = 1

stats = sorted([i for i in fandoms.items()], key=lambda x: x[1])

for fandom, count in stats:
	print("%s\t%s" % (str(count), fandom))
