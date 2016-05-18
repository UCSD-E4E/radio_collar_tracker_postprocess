#!/bin/bash
# Constant configuration
source /usr/bin/rct_bin_ref.sh

while getopts "src" opt; do
	case $opt in
		s)
			signal_dist_outpt=true
			;;
		r)
			record=true
			;;
		c)
			clean_run=true
			;;
	esac
done

# User supplied configuration
data_dir=`${FILE_CHOOSER} 2> /dev/null`
if [[ $data_dir == "None" ]]
then
	exit 1
fi

if [ "${clean_run}" = true ]
then
	if [[ -e ${data_dir}/RUN ]]
	then
		rm ${data_dir}/RUN
	fi
	if [[ -e ${data_dir}/ALT ]]
	then
		rm ${data_dir}/ALT
	fi
	if [[ -e ${data_dir}/COL ]]
	then
		rm ${data_dir}/COL
	fi
	exit 0
fi

if [[ -e ${data_dir}/RUN ]]
then
	run=`${META_FILE_READER} -i ${data_dir}/RUN -t run_num`
else
	run=`${RUN_NUM_CHOOSER}`
	if [[ "None" == $run ]]
	then
		exit 1
	fi
fi

if [ "${record}" = true ]
then
	echo "run_num: ${run}" > ${data_dir}/RUN
fi

if [[ -e ${data_dir}/ALT ]]
then
	flt_alt=`${META_FILE_READER} -i ${data_dir}/ALT -t flt_alt`
else
	flt_alt=`${FLT_ALT}`
	if [[ "None" == $flt_alt ]]
	then
		exit 1
	fi
fi

if [ "${record}" = true ]
then
	echo "flt_alt: ${flt_alt}" > ${data_dir}/ALT
fi

if [[ -e ${data_dir}/COL ]]
then
	cp ${data_dir}/COL ${CONFIG_DIR}/COL
else
	${COLLAR_CHOOSER} > ${CONFIG_DIR}/COL
	col_res=$?
	if ! [[ $col_res == 0 ]]
	then
		exit 1
	fi
fi

if [ "${record}" = true ]
then
	cp ${CONFIG_DIR}/COL ${data_dir}/COL
fi

# Generated variables
num_raw_files=`ls ${data_dir} | grep 'RAW_DATA_' | wc -l`
num_collars=`cat ${CONFIG_DIR}/COL | wc -l`
raw_file=`printf "%s/RUN_%06d.raw" ${data_dir} ${run}`
collar_file_prefix=`printf "%s/RUN_%06d_" ${data_dir} ${run}`
meta_file=`printf "%s/META_%06d" ${data_dir} ${run}`
sdr_center_freq=`${META_FILE_READER} -i ${meta_file} -t center_freq`
sdr_ppm=`${META_FILE_READER} -i ${CONFIG_DIR}/SDR.cfg -t sdr_ppm`

# # Concatenate raw files together
# if [[ -e $raw_file ]]
# then
# 	rm ${raw_file}
# fi
# ${CAT_RELEVANT} -i ${data_dir} -r ${run}
# if ! [[ $? -eq 0 ]]
# then
# 	exit 1
# fi

# Run through GNU Radio pipeline for each collar
for i in `seq 1 ${num_collars}`
do
	# Get collar beat frequency
	frequency=`${META_FILE_READER} -i ${CONFIG_DIR}/COL -t ${i}`
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
	beat_freq=`${FREQUENCY_CALCULATOR} -f ${sdr_center_freq} -c ${frequency} -e ${sdr_ppm}`
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
	# Execute pipeline
	${GNU_RADIO_PIPELINE} -f ${beat_freq} -i ${data_dir} -o `printf "%s%06d.raw" ${collar_file_prefix} ${i}` -r ${run}
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
	${RAW_DATA_COMPILER} -i ${data_dir} -o ${data_dir} -r ${run} -c ${i} -a ${flt_alt}
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
done

# For each collar, make map
for i in `seq 1 ${num_collars}`
do
	data_file=`printf '%s/RUN_%06d_COL_%06d.csv' ${data_dir} ${run} ${i}`
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
	${DISPLAY_DATA} -i ${data_file} -o ${data_dir} -r ${run} -n ${i} -c ${CONFIG_DIR}/COL
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
	if [ "$signal_dist_outpt" = true ]
	then
		${SIGNAL_DISTANCE_DISPLAY_DATA} -i ${data_file} -o ${data_dir} -r ${run} -n ${i} -c ${CONFIG_DIR}/COL
	fi
	if ! [[ $? -eq 0 ]]
	then
		exit 1
	fi
done

rm ${data_dir}/*.raw
