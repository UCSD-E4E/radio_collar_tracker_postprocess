#!/bin/bash
ppm=`python_dialogs/getSDRppm.py`
echo "sdr_ppm: $ppm" > config/SDR.cfg
