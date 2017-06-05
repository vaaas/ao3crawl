#!/bin/sh

if test -z "$1" || test -z "$2"
then
	echo 'usage: crawl.sh start_url count'
fi

python3 crawler.py "$1" "$2" | xz --verbose - >> /var/tmp/metadata.txt.xz 
