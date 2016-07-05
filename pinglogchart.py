#!/usr/bin/python
" turns the pinglog *.dat files into a picture "
# remember: 0 is no measurement, -1 is timeout,
#  and -2 is socket not available (cable unplugged)
from __future__ import print_function
import struct, sys
from PIL import Image, ImageDraw
# do I use matlab, or just make my own?

SHORTINT = struct.Struct('!h')


def file_to_list(fobj):
  " file object should be a stream of short-ints, returns tuple of int "
  result = []
  while True:
    bytesin = fobj.read(SHORTINT.size)
    if not bytesin:
      break
    result.append(SHORTINT.unpack(bytesin)[0])
  return tuple(result)


def numlist_to_image(dataset, height=150):
  " returns PIL image object that is similar to a sparkline of the data "
  # assumes the dataset has numbers in the set (-2|-1|0|1-300)
  basey = height - (height // 20)
  # bottom 5% reserved for the red '-1' results
  # remember: PIL has (0,0) in the UPPER left corner
  img = Image.new("RGB", (len(dataset), height), 'white')
  draw = ImageDraw.Draw(img)
  for i in range(24):
    ulx = i * (img.size[0] // 24)
    draw.line((ulx, 0, ulx, height), fill='grey')
    draw.text((ulx, 0), str(i), fill='grey')
  for i in range(len(dataset)):
    ulx = i
    if dataset[i] == -1:
      # '-1' means connection to router is okay but ping did not respond
      # don't listen to the IDE; ImageDraw boxes are (west, north, east, south)
      draw.rectangle((ulx, basey, ulx, height), fill='red')
    elif dataset[i] == -2:
      # '-2' means the iface was down, or some other socket.error
      pass
    # elif dataset[i] == 0:
      # the program probably wasn't running
    elif dataset[i] > 0:
      uly = basey - (dataset[i] // 2)
      if uly < 0:
        uly = 0
      draw.rectangle((ulx, uly, ulx, basey), fill='green')
  return img

# -- main

if len(sys.argv) < 2:
  print("usage: %s xxxxxxxx.yyyymmdd.dat [ file2 file3 ...]")
  sys.exit(1)
for FNAME in sys.argv[1:]:
  if not FNAME.endswith('.dat'):
    raise Exception('bad filename: ' + FNAME)
  FOBJ = open(FNAME, 'rb')
  DATA = file_to_list(FOBJ)
  IMAGE = numlist_to_image(DATA)
  IMAGE.save(FNAME.replace('.dat', '.png'), 'PNG')
  if sys.stdin.isatty():
    NUM = sum([1 for i in DATA if (i !=0 and i != -2)])
    FAILS = sum([1 for i in DATA if (i == -1)])
    AVG = sum([i for i in DATA if (i > 0)])*1.0/NUM
    FAILRATE = FAILS*1.0/NUM * 100
    print("samples taken: {}".format(NUM))
    print("average ping: {:.0f}ms  drop rate: {:1.1f}%".format(AVG, FAILRATE))

