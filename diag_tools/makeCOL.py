#!/usr/bin/env python
import argparse
import os.path
import os

parser = argparse.ArgumentParser('Creates a new COL file based on a center frequency +/- a certain offset')
parser.add_argument('frequency')
parser.add_argument('offset')
parser.add_argument('step')
args = parser.parse_args();

if os.path.isfile('COL'):
	os.rename('COL', 'COL.old')
COL = open('COL', 'w')

offset = int(args.offset)
freq = int(args.frequency)
step = int(args.step)

for i in xrange(freq - offset, freq + offset, step):
	COL.write('%d\n' % i)
	

