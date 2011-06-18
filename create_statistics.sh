#!/bin/bash
#$ -o ~enwikt/statistics/logs/
#$ -j y

export PYTHONPATH=~enwikt/lib/python/

cd ~enwikt/statistics/
LATEST=`ls ~enwikt/public_html/definitions/ |sed -n '${x;p};{s/enwikt-defs-\([0-9]\{8\}\)-all.tsv.*/\1/;T;h}'`
DATE=${LATEST:0:4}-${LATEST:4:2}-${LATEST:6:2}

echo $LATEST > this_run

if [ "`diff -q this_run last_run`" -o "$1" = --force ]; then
	gunzip -c ~enwikt/public_html/definitions/enwikt-defs-$LATEST-all.tsv.gz |\
		python wt_stats.py - $DATE latest_stats &&\
			mv latest_stats ~enwikt/public_html/generated/statistics.txt &&\
				mv this_run last_run

fi
