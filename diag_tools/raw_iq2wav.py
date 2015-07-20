#!/usr/bin/env python

import struct

#fin = open('2015.07.12.BBBtest2')
#fin = open('iq')
fin = open('mba_test')
fout = open('SDRSharp_20150714_212203Z_172464kHz_IQ.wav', 'w')

def float32_wav_file(sample_array, sample_rate):
  byte_count = (len(sample_array)) * 4  # 32-bit floats
  wav_file = ""
  # write the header
  wav_file += struct.pack('<ccccIccccccccIHHIIHH',
    'R', 'I', 'F', 'F',
    byte_count + 0x2c - 8,  # header size
    'W', 'A', 'V', 'E', 'f', 'm', 't', ' ',
    0x10,  # size of 'fmt ' header
    3,  # format 3 = floating-point PCM
    2,  # channels
    sample_rate,  # samples / second
    sample_rate * 2 * 4,  # bytes / second
    8,  # block alignment
    32)  # bits / sample
  wav_file += struct.pack('<ccccI',
    'd', 'a', 't', 'a', byte_count)
  for sample in sample_array:
    wav_file += struct.pack("<f", sample)
  return wav_file

ary = [(float(ord(foo)) - 127.)/128. for foo in fin.read(1024*1024)]

fout.write(float32_wav_file(ary, 2048000))

fin.close()
fout.close()
