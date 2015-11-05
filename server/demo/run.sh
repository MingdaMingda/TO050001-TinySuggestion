#!/bin/bash -e

echo "begin"

export PYTHONPATH="../bin/"

echo "  stop..."
pid=`ps aux | fgrep "woo_tiny_sugg_demo.py" | fgrep -v grep  | awk '{print $2}'`
if [ "M$pid" != "M" ]; then
	echo "  kill $pid"
	kill -9 $pid

	echo "  sleep..."
	sleep 3
else
	echo " info: no running service, just start"
fi

echo "  start..."

python woo_tiny_sugg_demo.py 1>server.log 2>&1 &

echo "done."

