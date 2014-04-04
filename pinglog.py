#!/usr/bin/python
""" write to a file the ping response time, one signed-int per 5-second
    tries to sample every second, writes max unless there was a problem
    value of -1 means no response, -2 means socket error
    17kb file each day, starts a new file at midnight
"""
from __future__ import print_function
import ping, socket, struct, sys, time


def hostname_to_hex(remotehost):
  " returns eight-char hex string "
  addr = socket.gethostbyname(remotehost)
  return socket.inet_aton(addr).encode('hex')


def timeofday_coarse(grain=5):
  now = time.localtime()
  now = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
  return now // grain


def pingloop(remoteaddr, grain=5, verbose=False):
  " workhorse "
  fileplate = "%s-%%s.dat" % (hostname_to_hex(remoteaddr))
  oldday = '0'
  polls = [0]
  oldnow = timeofday_coarse(grain)
  outfile = None
  ZERO = struct.pack('!h', 0)
  while True:
    day = time.strftime('%Y%m%d')
    if day != oldday:
      # new day means new logfile
      if outfile is not None:
        outfile.close()
      filename = fileplate % day
      if verbose:
        print("Writing to %s" % filename)
      outfile = open(filename, 'wb')
      # fill the file with short-int zeroes, one for each chunk
      # TODO: what if grain doesn't divide evenly into 86400 ?
      outfile.write(ZERO * (24 * 60 * 60 // grain))
      outfile.seek(0)
      oldday = day
    now = timeofday_coarse()
    if now != oldnow:
      # write chunk
      polls.sort(reverse=True)
      score = polls[0]
      if len([-1 for i in polls if i == -1]) > 1:
        # if more than one failed pings, mark the whole chunk as failed
        score = -1
      outfile.seek(oldnow * len(ZERO))
      outfile.write(struct.pack('!h', score))
      polls = []
      oldnow = now
    try:
      pingtime = int((ping.do_one(remoteaddr, 1) or -.001) * 1000)
      polls.append(pingtime)
    except socket.error:
      # TODO: detect when we fail because we're not root and die
      # TODO: detect when we fail because no default iface and pass
      pingtime = -2
    polls.append(pingtime)
    if verbose:
      print("%s: %d" % (time.strftime('%H:%M:%S'), pingtime), end='\n')
#      if (pingtime < 0 or pingtime > 300):
#        print("%s: %d" % (time.strftime('%H:%M:%S'), pingtime), end='\n')
#      else:
#        print("%s: %d" % (time.strftime('%H:%M:%S'), pingtime), end='\r')
    time.sleep(1)


if len(sys.argv) != 2:
  print("Usage: pinglog remotehost")
  sys.exit(1)
ADDR = socket.gethostbyname(sys.argv[1])
if ADDR is None:
  raise Exception("bad hostname %s" % sys.argv[1])

pingloop(ADDR, verbose=True)
