#!/usr/bin/env python
## Takes in a RCT Run folder name and prints the run number to stdout

import argparse

parser = argparse.ArgumentParser(description='Takes in a RCT Run directory and '
	'prints the run number of that directory to stdout')
parser.add_argument('dir_name', help='RCT Run directory')

args = parser.parse_args()

run_num = int(args.dir_name.strip().rstrip('/').rpartition('/')[2].rpartition('_')[2])
print(run_num)
