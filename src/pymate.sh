#!/bin/bash

cd "`dirname $0`"
if test -f "./pminit.py"; then
	exec python2 "./pminit.py" $@
else
	cd "/usr/share/pymate"
	exec python2 "./pminit.py" $@
fi
