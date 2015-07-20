#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser('')
parser.add_argument('bin')
args = parser.parse_args()

bin = int(args.bin)
pul_num_sam = 40960
f_samp = 2048000
center_freq = 172464000
freq = (float(bin) / pul_num_sam - 0.5) * f_samp + center_freq
print(freq)
