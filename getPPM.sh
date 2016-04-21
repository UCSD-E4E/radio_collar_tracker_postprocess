#!/bin/bash
ppm=`python_dialogs/getSDRppm.py`
if ! [[ $? -eq 0 ]]
then
	exit 1
fi
echo "sdr_ppm: $ppm" > config/SDR.cfg
