#!/usr/bin/env python
import math
import argparse

parser = argparse.ArgumentParser('')
parser.add_argument('frequency')
args = parser.parse_args()

frequency = int(args.frequency)
frequency = frequency + 11000
frequency = frequency - 172464000
pul_num_sam = 40960
f_samp = 2048000
bin = int(math.ceil(pul_num_sam / 2 + float(pul_num_sam) * float(frequency) / f_samp + 1))
print(bin)
