#!/bin/bash
# Ping.  Carp if the ping toggles between succ & fail

REMOTE_ADDR="8.8.8.8"  # change to something apropos for your site
PING=/sbin/ping
PING_OPTS="-c1 -t1"

let TOGGLETIME=-1
let OLDEXIT=-1
while true; do  # Ctrl-C to stop, obviously
  $PING $PING_OPTS $REMOTE_ADDR >/dev/null 2>/dev/null
  NEWEXIT=$?
  if [ $OLDEXIT == -1 ]; then
    echo "$(date) Starting monitoring"
    let OLDEXIT=NEWEXIT
  elif [ $NEWEXIT != $OLDEXIT ]; then
    NOW=$(date +%s)
    if [ $NEWEXIT == 0 ]; then
      echo "... $(( $NOW - $TOGGLETIME )) seconds."
    else
      echo -n "$(date) DOWN "
    fi
    let OLDEXIT=NEWEXIT
    let TOGGLETIME=NOW
  fi
  sleep 5
done

