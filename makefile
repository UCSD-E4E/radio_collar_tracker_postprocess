SHELL=/bin/bash
.PHONY: clean all install uninstall configure

all: fft_detect/fft_detect

configure: config/SDR.cfg config

config:
	mkdir config

install: fft_detect/fft_detect raw_gps_analysis/raw_gps_analysis.py\
	collarDisplay/display_data.py meta_file_reader/read_meta_file.py\
	ppm_adjust/get_beat_frequency.py config/SDR.cfg\
	python_dialogs/filechooser.py python_dialogs/getRunNum.py\
	python_dialogs/getCollars.py CLI_GUI/cat_relevant.py\
	python_dialogs/getFltAlt.py CLI_GUI/cas2.sh rct_bin_ref.sh
	cp rct_bin_ref.sh /usr/bin/rct_bin_ref.sh
	chmod +x /usr/bin/rct_bin_ref.sh
	cp CLI_GUI/cas2.sh /usr/bin/rct_cas
	chmod +x /usr/bin/rct_cas

rct_bin_ref.sh:
	echo "#!/bin/bash" > rct_bin_ref.sh
	echo GNU_RADIO_PIPELINE=\'$(CURDIR)/fft_detect/fft_detect\' >> rct_bin_ref.sh
	echo RAW_DATA_COMPILER=\'$(CURDIR)/raw_gps_analysis/raw_gps_analysis.py\' >> rct_bin_ref.sh
	echo DISPLAY_DATA=\'$(CURDIR)/collarDisplay/display_data.py\' >> rct_bin_ref.sh
	echo SIGNAL_DISTANCE_DISPLAY_DATA=\'$(CURDIR)/collarDisplay/signal_distance_angle.py\' >> rct_bin_ref.sh
	echo META_FILE_READER=\'$(CURDIR)/meta_file_reader/read_meta_file.py\' >> rct_bin_ref.sh
	echo FREQUENCY_CALCULATOR=\'$(CURDIR)/ppm_adjust/get_beat_frequency.py\' >> rct_bin_ref.sh
	echo CONFIG_DIR=\'$(CURDIR)/config/\' >> rct_bin_ref.sh
	echo FILE_CHOOSER=\"$(CURDIR)/python_dialogs/filechooser.py\" >> rct_bin_ref.sh
	echo RUN_NUM_CHOOSER=\"$(CURDIR)/python_dialogs/getRunNum.py\" >> rct_bin_ref.sh
	echo COLLAR_CHOOSER=\"$(CURDIR)/python_dialogs/getCollars.py\" >> rct_bin_ref.sh
	echo CAT_RELEVANT=\'$(CURDIR)/CLI_GUI/cat_relevant.py\' >> rct_bin_ref.sh
	echo FLT_ALT=\'$(CURDIR)/python_dialogs/getFltAlt.py\' >> rct_bin_ref.sh

clean:
	make -C fft_detect clean
	-rm rct_bin_ref.sh
	-rm config/COL
	-rm config/SDR.cfg
	-rm -rf config

uninstall:
	-rm config/SDR.cfg
	-rm config/COL
	-rmdir config
	make -C fft_detect clean
	-rm rct_bin_ref.sh
	-rm /usr/bin/rct_bin_ref.sh
	-rm /usr/bin/rct_cas

fft_detect/fft_detect: fft_detect/fft_detect.cpp
	make -C fft_detect

config/SDR.cfg:
	ppm=`python_dialogs/getSDRppm.py`
	-mkdir config
	echo 'sdr_ppm: ${ppm}' > config/SDR.cfg
