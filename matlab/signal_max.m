clear all
close all

FFT_LENGTH = 4096;
SAMPLE_RATE = 2000000;
SIG_LENGTH = int16(0.06 * SAMPLE_RATE / FFT_LENGTH);

run_dir = '/tmp/sdr_data';
ofile = '/tmp/sdr_data';
freq_bin = 901;
run_num = 1;

raw_files = dir([run_dir, '/RAW_DATA_*']);

maxSig = 0;

for file_idx = 1:length(raw_files)
	data = raw2complex(fullfile(raw_files(file_idx).folder, raw_files(file_idx).name));
	maxSig = max(maxSig, max(data));
end
disp(maxSig);
