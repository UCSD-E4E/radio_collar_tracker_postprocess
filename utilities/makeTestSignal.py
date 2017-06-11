#!/usr/bin/env python
import argparse
import numpy as np
import os

def getLengthFromGPS(run_dir, run_num):
    filename = "%s/GPS_%06d" % (run_dir, run_num)
    names = ['time', 'lat', 'lon', 'col', 'alt']
    data = np.genfromtxt(filename, delimiter=',', names=names)
    start_time = np.amin(data['time'])
    end_time = np.amax(data['time'])
    return end_time - start_time    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generates a test signal to replace existing data')
    parser.add_argument('-d', '--dir', required = True, dest = 'run_dir', help = 'Data directory')
    parser.add_argument('-r', '--run_num', required = True, type = int, dest = 'run_num', help = 'Run number')
    parser.add_argument('-f', '--freq', required = True, type = int, dest = 'freq', help = 'Test frequency')
    parser.add_argument('-s', '--samp_freq', required = False, type = int, default = 2048000, dest = 'samp_freq', help = 'Sampling frequency')

    args = parser.parse_args()
    run_dir = args.run_dir
    run_num = args.run_num
    freq = args.freq
    samp_freq = args.samp_freq

    sig_length = getLengthFromGPS(run_dir, run_num)

    data = np.arange(0, 20971520 / 2, dtype = complex)
    data = data / samp_freq
    data = np.cos(data) + 1j * np.sin(data)
    data = data * 128 + 128
    byte_data = [(int(x.real), int(x.imag)) for x in data]

    raw_files = sorted([file for file in os.listdir(run_dir) if file.startswith('RAW_DATA_%06d' % run_num)])
