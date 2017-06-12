#!/bin/sh

if test -z "$1"
then
	echo 'please point first argument to the data'
	exit 1
fi

for i in analysis/*py
do
	python3 "$i" < $1 > "outputs/$(basename "$i").txt"
	echo "$(basename "$i") done"
done
