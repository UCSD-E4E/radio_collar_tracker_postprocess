#!/bin/bash
META_FILE_READER="/Users/e4e/e4e-rct/radio_collar_tracker/meta_file_reader/read_meta_file.py"
FILE_CHOOSER="/Users/e4e/e4e-rct/radio_collar_tracker/python_dialogs/filechooser.py"
DECREMENTER="/Users/e4e/e4e-rct/radio_collar_tracker/downloader/decrementer.py"

# Get fileCount
scp -i ~/.ssh/id_rsa pi@192.168.2.129:~/rct/fileCount ./fileCount > /dev/null
# Get run number
run_num=`${META_FILE_READER} -i ./fileCount -t currentRun | ${DECREMENTER}`
# Make directory
output_dir=`${FILE_CHOOSER} 2> /dev/null`
# Download data
scp -i ~/.ssh/id_rsa pi@192.168.2.129:~/rct/*${run_num}* ${output_dir} > /dev/null
rm ./fileCount
