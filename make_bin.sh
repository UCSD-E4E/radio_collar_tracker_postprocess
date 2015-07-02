#!/bin/bash
cwd=$(pwd)
if [ ! -d "$HOME/rct/bin/" ] ; then
	mkdir -p $HOME/rct/bin/
fi
cd ${cwd}/CurrentCode/PostProcessC/
chmod +x build*
./build-spectrumAnalysis

cd ${cwd}
cp ${cwd}/collarDetect/altFilter.py $HOME/rct/bin/
cp ${cwd}/CurrentCode/PostProcessC/spectrumAnalysis $HOME/rct/bin/
cp ${cwd}/CLI_GUI/cas.sh $HOME/rct/bin/
cp ${cwd}/CLI_GUI/get_run_num.py $HOME/rct/bin/
chmod +x $HOME/rct/bin/*
