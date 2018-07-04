#!/bin/sh
if [ `ps ax|grep "python tsukutter.py$"|wc|awk '{print $1}'` -ge 1 ];
then
	echo "Nothing"
else
	cd /app/bat
	echo "(re)start tukutter"
	python tsukutter.py
fi
