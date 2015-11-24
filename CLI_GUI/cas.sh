#! /usr/bin/env bash
if [[ $1 -eq "-h" || $1 -eq "--help" ]] ; then
	echo "Usage: cas.sh run flight_alt data_dir"
	echo ""
	echo "run             Run number"
	exit 0
fi
if [ $# -ne 1 ]; then
	echo "Invalid arguments! Usage: cas.sh run flight_alt data_dir"
	echo ""
	echo "run             Run number"
	exit 1
fi

# read -e -p "Enter Raw Data directory: " dir
dir=$1
if ! [[ -d $dir ]]; then
	echo "Invalid arguments! Usage: cas.sh run flight_alt data_dir"
	echo ""
	echo "run             Run number"
	exit 1
fi
dir=$(echo $dir | sed "s%~%$HOME%")

run=$(get_run_num.py $dir)
echo $run

# read -p "Enter flight altitude: " alt
alt='30'
if [[ -w JOB ]]; then
	rm JOB
fi
if [ -e "COL" ]
then
	echo "Collar definitions found!"
else
	echo "Collar definitions not found!"
	exit 1
fi
num_col=$(cat COL | wc -l)
echo $dir"/" >> JOB
echo "curr_run: "$run >> JOB
echo "freq_em: 1000" >> JOB
echo "pulse_ms: 20" >> JOB
echo "lin_scale: 1" >> JOB
echo "map_d: 128" >> JOB
echo "alpha_c_thres: 500" >> JOB
echo "num_col: "$num_col >> JOB
echo "f_drift: 11000" >> JOB
if [ -e "spectrumAnalysis" ]
then
	./spectrumAnalysis > /dev/null
else
	if [ -e "build-spectrumAnalysis" ]
	then
		./build-spectrumAnalysis
		./spectrumAnalysis > /dev/null
	else
		echo "Could not find ./spectrumAnalysis!"
	fi
fi
runFile=$(ls | grep -E RUN_[[:digit:]]\+$run.csv$)
./altFilter.py $alt $runFile
./display_data.py $runFile
