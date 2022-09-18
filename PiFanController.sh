#!/bin/bash
# System-V service file
#

SERVICE_NAME="RPi Fan Controller"
SERVICE_ID="PiFanController"

SERVICE_PATH=/home/TTra/python/PiFanController

function d_start()
{
	echo "Start Service: $SERVICE_NAME"
	cd $SERVICE_PATH
	/usr/bin/python3 $SERVICE_ID.py &
	sleep 1
	echo "PID is $(cat /tmp/$SERVICE_ID.pid)"
}

function d_stop()
{
	echo "Stop Service: $SERVICE_NAME (PID = $(cat /tmp/$SERVICE_ID.pid))"
	kill $(cat /tmp/$SERVICE_ID.pid)
	rm /tmp/$SERVICE_ID.pid
}

function d_status()
{
	ps -ef | grep $SERVICE_ID | grep -v grep
	echo "PID indicate indication file $(cat /tmp/$SERVICE_ID.pid 2> /dev/null)"
}

# Management instructions of the service
case "$1" in
	start)
		d_start
		;;
	stop)
		d_stop
		;;
	reload)
		d_stop
		sleep 1
		d_start
		;;
	status)
		d_status
		;;
	*)
	echo "Usage: $0 {start | stop | reload | status}"
	exit 1
	;;
esac

exit  0