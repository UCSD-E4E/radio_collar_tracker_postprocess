#!/usr/bin/env python

import struct

#fin = open('2015.07.12.BBBtest2')
#fin = open('iq')
fin = open('rtl_sdr_raw.raw')
fout = open('SDRSharp_20150720_212203Z_172500kHz_IQ.wav', 'w')


# Sourced from http://stackoverflow.com/questions/15576798/create-32bit-float-wav-file-in-python
def float32_wav_file(sample_array, sample_rate):
  byte_count = (len(sample_array)) * 4  # 32-bit floats
  wav_file = ""
  # write the header
  wav_file += struct.pack('<ccccIccccccccIHHIIHH',
    'R', 'I', 'F', 'F', #cccc
    byte_count + 0x2c - 8,  # header size I
    'W', 'A', 'V', 'E', 'f', 'm', 't', ' ', #cccccccc
    0x10,  # size of 'fmt ' header  #I
    3,  # format 3 = floating-point PCM #H
    2,  # channels  #H
    sample_rate,  # samples / second  #I
    sample_rate * 2 * 4,  # bytes / second  #!
    8,  # block alignment #H
    32)  # bits / samples #H
  wav_file += struct.pack('<ccccI',
    'd', 'a', 't', 'a', byte_count)
  for sample in sample_array:
    wav_file += struct.pack("<f", sample)
  return wav_file

ary = [(float(ord(foo)) - 127.)/128. for foo in fin.read(1024*1024)]

#switch i and q
for i in xrange(0, len(ary), 2):
  temp = ary[i + 1]
  ary[i + 1] = ary[i]
  ary[i] = temp

fout.write(float32_wav_file(ary, 2048000))

fin.close()
fout.close()
