#!/bin/bash
# Constant configuration
GNU_RADIO_PIPELINE='/Users/e4e/e4e-rct/radio_collar_tracker/cw_detect/cw_detect_deploy.py'
RAW_DATA_COMPILER='/Users/e4e/e4e-rct/radio_collar_tracker/raw_gps_analysis/raw_gps_analysis.py'
DISPLAY_DATA='/Users/e4e/e4e-rct/radio_collar_tracker/collarDisplay/display_data.py'
META_FILE_READER='/Users/e4e/e4e-rct/radio_collar_tracker/meta_file_reader/read_meta_file.py'
FREQUENCY_CALCULATOR='/Users/e4e/e4e-rct/radio_collar_tracker/ppm_adjust/get_beat_frequency.py'
CONFIG_DIR='/Users/e4e/e4e-rct/radio_collar_tracker/config/'
FILE_CHOOSER="/Users/e4e/e4e-rct/radio_collar_tracker/python_dialogs/filechooser.py"
RUN_NUM_CHOOSER="/Users/e4e/e4e-rct/radio_collar_tracker/python_dialogs/getRunNum.py"
COLLAR_CHOOSER="/users/e4e/e4e-rct/radio_collar_tracker/python_dialogs/getCollars.py"

# User supplied configuration
data_dir=`${FILE_CHOOSER} 2> /dev/null`
if [[ $data_dir == "None" ]]
then
	exit 1
fi	
run=`${RUN_NUM_CHOOSER}`
if [[ "None" == $run ]]
then
	exit 1
fi	
${COLLAR_CHOOSER} > ${CONFIG_DIR}/COL
col_res=$?
if ! [[ $col_res == 0 ]]
then
	exit 1
fi

# Generated variables
num_raw_files=`ls ${data_dir} | grep 'RAW_DATA_' | wc -l`
num_collars=`cat ${CONFIG_DIR}/COL | wc -l`
raw_file=`printf "%s/RUN_%06d.raw" ${data_dir} ${run}`
collar_file_prefix=`printf "%s/RUN_%06d_" ${data_dir} ${run}`
meta_file=`printf "%s/META_%06d" ${data_dir} ${run}`
sdr_center_freq=`${META_FILE_READER} -i ${meta_file} -t center_freq`
sdr_ppm=`${META_FILE_READER} -i ${CONFIG_DIR}/SDR.cfg -t sdr_ppm`

# Concatenate raw files together
if [[ -e $raw_file ]]
then
	rm ${raw_file}
fi
for i in `seq 1 ${num_raw_files}`
do
	cat `printf "%s/RAW_DATA_%06d_%06d" ${data_dir} ${run} ${i}` >> ${raw_file}
done

# Run through GNU Radio pipeline for each collar
for i in `seq 1 ${num_collars}`
do
	# Get collar beat frequency
	frequency=`${META_FILE_READER} -i ${CONFIG_DIR}/COL -t ${i}`
	beat_freq=`${FREQUENCY_CALCULATOR} -f ${sdr_center_freq} -c ${frequency} -e ${sdr_ppm}`
	# Execute pipeline
	${GNU_RADIO_PIPELINE} -f ${beat_freq} -i ${raw_file} -o `printf "%s%06d.raw" ${collar_file_prefix} ${i}`
	${RAW_DATA_COMPILER} -i ${data_dir} -o ${data_dir} -r ${run} -c ${i}
done

# For each collar, make map
for i in `seq 1 ${num_collars}`
do
	data_file=`printf '%s/RUN_%06d_COL_%06d.csv' ${data_dir} ${run} ${i}`
	${DISPLAY_DATA} -i ${data_file} -o ${data_dir} -r ${run} -c ${i}
done
