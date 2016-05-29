SHELL=/bin/bash
.PHONY: clean all install uninstall configure fft_detect/fft_detect

all: fft_detect/fft_detect

configure: config/SDR.cfg config

config:
	mkdir config
	chmod a+rwx config

install: fft_detect/fft_detect raw_gps_analysis/raw_gps_analysis.py\
	collarDisplay/display_data.py meta_file_reader/read_meta_file.py\
	ppm_adjust/get_beat_frequency.py config/SDR.cfg\
	python_dialogs/fileChooser.py python_dialogs/getRunNum.py\
	python_dialogs/getCollars.py CLI_GUI/cat_relevant.py\
	python_dialogs/getFltAlt.py CLI_GUI/cas2.sh utilities/makeShapefile.py\
	collarDisplay/csvToShp.py

	cp CLI_GUI/rct_cas.py /usr/local/bin/rct_cas
	chmod +x /usr/local/bin/rct_cas
	cp raw_gps_analysis/raw_gps_analysis.py /usr/local/bin/
	cp collarDisplay/display_data.py /usr/local/bin/
	cp meta_file_reader/read_meta_file.py /usr/local/bin/
	cp ppm_adjust/get_beat_frequency.py /usr/local/bin/
	-mkdir /usr/local/etc/rct/
	cp config/SDR.cfg /usr/local/etc/rct/
	cp python_dialogs/fileChooser.py /usr/local/bin/
	cp python_dialogs/getRunNum.py /usr/local/bin/
	cp python_dialogs/getCollars.py /usr/local/bin/
	cp python_dialogs/getFltAlt.py /usr/local/bin/
	cp fft_detect/fft_detect /usr/local/bin/
	cp utilities/makeShapefile.py /usr/local/bin/makeShapefile
	cp collarDisplay/csvToShp.py /usr/local/bin/


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

rct_bin_ref.py:
	echo "#!/usr/bin/env python" > rct_bin_ref.py
	echo GNU_RADIO_PIPELINE=\'$(CURDIR)/fft_detect/fft_detect\' >> rct_bin_ref.py
	echo CONFIG_DIR=\'$(CURDIR)/config/\' >> rct_bin_ref.py

clean:
	make -C fft_detect clean
	-rm -f rct_bin_ref.sh
	-rm config/COL
	-rm config/SDR.cfg
	-rm -rf config

uninstall:
	-rm -rf /usr/local/etc/rct/
	make -C fft_detect clean
	-rm rct_bin_ref.*
	-rm /usr/local/bin/rct_cas
	-rm /usr/local/bin/raw_gps_analysis.py
	-rm /usr/local/bin/display_data.py
	-rm /usr/local/bin/read_meta_file.py
	-rm /usr/local/bin/get_beat_frequency.py
	-rm /usr/local/etc/rct/SDR.cfg
	-rm -rf /usr/local/etc/rct/
	-rm /usr/local/bin/fileChooser.py
	-rm /usr/local/bin/getRunNum.py
	-rm /usr/local/bin/getCollars.py
	-rm /usr/local/bin/getFltAlt.py
	-rm /usr/local/bin/fft_detect
	-rm /usr/local/bin/makeShapefile
	-rm /usr/local/bin/csvToShp.py

fft_detect/fft_detect:
	make -C fft_detect

config/SDR.cfg: config
	./getPPM.sh
