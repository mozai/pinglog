pinglog
=======

I'm having trouble with my ISP connection dropping out.  I want to record
when it happens, and make a picture of it, so I can quickly eyeball a
few days's worth of data an use my meatbrain's pattern-matching abilities.

Also so I can show the pictures to other meatbrains, to prove that my
meatbrain isn't hallucinating.

Use
---
Since it needs to send out and listen for ICMP messages, it'll need to run
as root.  Sorry about that.  Find the IP address of a host that is just one
or two hops past your router, someplace nice and close that most of your
traffic will go through.

    python ./pinglog.py 192.168.0.10

I leave that running in a terminal window, so when my webbrowser or
streaming music or backup rsync hangs, I can see if it's just that
program or if it's the net connection.

It will log the data to files named 'xxxxxxxx.yyyymmdd.dat', where 'xxxxxxxx'
is the hex octets of the ip address you gave it.  It will make new files
each new day.  After you've got a few day's worth, you can make the graphs
with:

    python ./pingloggraph.py xxxxxxxx.yyyymmdd.dat

This will make a xxxxxxxx.yyyymmdd.png file; I run `optipng` on it, then
open it up in an image viewer.  Each pixel on the x axis is a 5-second block
of time for the day.  Green bars are ping time (max 300ms), red bars are where
a ping was attempted but there wasn't a response.  White areas are where a
measurement couldn't be taken (maybe you unplugged the net cable, or maybe
you weren't running the program).  Added grey bars for the hour of the day
because the image is probably wider than your monitor and I doubt you can
intuitively detect where 4:13pm is with just your eyeball.

