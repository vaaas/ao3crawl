#!/bin/sh
python3 crawler.py "$1" "$2" | gzip --best -f - >> /var/tmp/ao3log.txt.gz 
