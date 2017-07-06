%% getOriginalSignal: Gets original signal from run directory
function [signal] = getOriginalSignal(run_dir, run_num, start_time, signal_length, sampling_rate)
	raw_files = dir([run_dir, '/RAW_DATA_*']);
	fileLen = round(raw_files(1).bytes / 4);
	fileNum = floor(start_time * sampling_rate / double(fileLen)) + 1;
	fileOffset = round(mod(start_time * sampling_rate, fileLen));
	endIndex = round(fileOffset + signal_length * sampling_rate - 1);
	nextFile = 0;
	if (fileOffset + signal_length * sampling_rate - 1) > fileLen
		endIndex = fileLen;
		nextFile = round(fileOffset + signal_length * sampling_rate - 1 - fileLen);
	end
	data = raw2complex(fullfile(raw_files(fileNum).folder, raw_files(fileNum).name));
	signal = data(fileOffset:endIndex);
	if nextFile ~= 0
		data = raw2complex(fullfile(raw_files(fileNum + 1).folder, raw_files(fileNum).name));
		signal = [signal; data(1:nextFile)];
	end