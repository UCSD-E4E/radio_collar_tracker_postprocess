	clear all
close all

FFT_LENGTH = 4096;
SAMPLE_RATE = 2000000;
OUTPUT_SAMPLE_RATE = SAMPLE_RATE / FFT_LENGTH;
SIG_LENGTH = int16(0.015 * SAMPLE_RATE / FFT_LENGTH);
collar_Freq = 172170500;
% collar_Freq = 172270500;
center_freq = 172500000;

run_dir = '/home/ntlhui/workspace/2017.08.CI_Deployment/2017.08.19/RUN_000022';
ofile = '/home/ntlhui/workspace/2017.08.CI_Deployment/2017.08.19/RUN_000022';
freq_bin = round((collar_Freq - center_freq) / SAMPLE_RATE * FFT_LENGTH);
if freq_bin < 1
	freq_bin = FFT_LENGTH + freq_bin
end
run_num = 22;

raw_files = dir([run_dir, '/RAW_DATA_*']);
gps_file = sprintf('%s/GPS_%06d', run_dir, run_num);
gps_data = csvread(gps_file);
meta_filename = sprintf('%s/META_%06d', run_dir, run_num);
meta_fh = fopen(meta_filename, 'r');
sdr_start_time = textscan(meta_fh, 'start_time: %f');

output_signal = [];
leftovers = [];

for file_idx = 1:min(15, length(raw_files))
	data = [leftovers; raw2complex(fullfile(raw_files(file_idx).folder, raw_files(file_idx).name))];
	for start_idx = 1:FFT_LENGTH:length(data)
		fft_buffer_in = data(start_idx:start_idx + FFT_LENGTH - 1);
		fft_buffer_out = fft(fft_buffer_in);
		% fft_buffer_out = [fft_buffer_out(FFT_LENGTH / 2 + 1 : FFT_LENGTH) fft_buffer_out(1:FFT_LENGTH / 2)];
		output_signal = [output_signal; (fft_buffer_out(freq_bin))];
	end
	leftovers = data(start_idx + FFT_LENGTH:length(data));
end
clear fft_buffer_out fft_buffer_in leftovers file_idx;

for i = 1:(length(output_signal) - 9)
	output_signal(i) = median(output_signal(i:i+9));
end
clear i;


figure;

% plotting the filtered signal
plot(1/OUTPUT_SAMPLE_RATE:1/OUTPUT_SAMPLE_RATE:length(output_signal)/OUTPUT_SAMPLE_RATE, 10 * log10(abs(output_signal)))
hold on;
collar_candidate = [];
for i = 1 : int64(2 * OUTPUT_SAMPLE_RATE) : int64(length(output_signal) / int64(2 * OUTPUT_SAMPLE_RATE) - 2) * int64(2 * OUTPUT_SAMPLE_RATE)
	collar_candidate = [collar_candidate; max(abs(output_signal(i:i+int64(2 * OUTPUT_SAMPLE_RATE) - 1)))];
end

% Plot the collar candidate threshold
% plot(1:2:length(collar_candidate) * 2 - 1, 10 * log10(abs(collar_candidate)));

% Generate the histogram based threshold
[counts, edges] = histcounts(10 * log10(abs(output_signal)), 15);
count_threshold = 0;
for i = length(counts):-1:1
	if counts(i) > mean(counts)
		count_threshold = edges(i + 1);
		break
	end
end
count_threshold = 10 * log10(rms(abs(output_signal)));
refline(0, count_threshold);
clear i;

% Find pings based on histogram threshold
ping_times = find(10 * log10(abs(output_signal)) > count_threshold);
ping_starts = [ping_times(1)]; % in OUTPUT_SAMPLE_RATE
for i = 1:length(ping_times) - 1
	if ping_times(i + 1) - ping_times(i) > 1
		ping_starts = [ping_starts; ping_times(i + 1)];
	end
end
clear i;

% Eliminate pings that aren't long enough
pings_to_remove = [];
ping_lengths = [];
for i = 1:length(ping_starts)
	ping_samples = ping_times(ping_times > ping_starts(i) & ping_times < (ping_starts(i) + 0.5 * OUTPUT_SAMPLE_RATE));
	if range(ping_samples) < 0.010 * OUTPUT_SAMPLE_RATE
		pings_to_remove = [pings_to_remove; i];
	else
		ping_lengths = [ping_lengths; range(ping_samples)];
	end
end
ping_starts(pings_to_remove) = [];

[ping_counts, ping_lengths_edges] = histcounts(ping_lengths);
ping_counts = round(ping_counts / (max(ping_counts) / 100));
ping_count_threshold = find(ping_counts > 0, 1);
ping_starts(ping_lengths < ping_count_threshold) = [];
ping_lengths(ping_lengths < ping_count_threshold) = [];

disp(ping_lengths);
disp(length(ping_starts) == length(ping_lengths))
clear i ping_samples pings_to_remove;

% plot 50 ms RMS values
rms_interval = round(0.2 * OUTPUT_SAMPLE_RATE);
for i = 1:rms_interval:length(output_signal) - rms_interval
	rms_signal(round(i / rms_interval) + 1) = rms(output_signal(i:i+rms_interval));
end
plot(1/(OUTPUT_SAMPLE_RATE / rms_interval):1/(OUTPUT_SAMPLE_RATE/rms_interval): length(rms_signal) / (OUTPUT_SAMPLE_RATE / rms_interval), 10 * log10(abs(rms_signal)))


% % Get frequency of pings
% ping_frequencies = [];
% for i = 1:length(ping_starts)
% 	start_time = ping_starts(i) / OUTPUT_SAMPLE_RATE;
% 	ping_signal = getOriginalSignal(run_dir, run_num, start_time, 0.010, SAMPLE_RATE);
% 	guess = 172951000;
% 	freq = getFrequencyOfPing(ping_signal, SAMPLE_RATE, guess);
% 	ping_frequencies = [ping_frequencies; freq];
% end
% probable_frequency = int64(median(ping_frequencies));
% clear i start_time ping_signal guess freq;

% % Get periods of pings
% periods = []; %in OUTPUT_SAMPLE_RATE
% for i = 1:length(ping_starts) - 1
% 	periods = [periods; ping_starts(i + 1) - ping_starts(i)];
% end
% clear i;
% periods = periods(periods > 0.5 * OUTPUT_SAMPLE_RATE);
% periods = periods ./ round(periods / min(periods));
% median_period = median(periods);
% periods = periods(periods < 1.1 * median_period);
% periods = periods(periods > 0.9 * median_period);
% period = mean(periods);
% clear periods median_period;

% % Circle all known pings
% t_out = 1/OUTPUT_SAMPLE_RATE:1/OUTPUT_SAMPLE_RATE:length(output_signal) / OUTPUT_SAMPLE_RATE;

% % Get GPS data for all pings
% gps_x = [];
% gps_y = [];
% gps_t = [];
% gps_v = [];
% gps_start = gps_data(1, 1);
% ping_window = 8;
% for i = 1:length(ping_starts)
% 	max_sample_idx = min(length(output_signal), ping_starts(i) + ping_window);
% 	min_sample_idx = max(1, ping_starts(i) - ping_window);
% 	[gps_v_raw, gps_v_rIDX] = max(output_signal(min_sample_idx:max_sample_idx));
% 	gps_v_rIDX = gps_v_rIDX + ping_starts(i) - ping_window;
% 	ping_offset_i = gps_v_rIDX / OUTPUT_SAMPLE_RATE;
% 	ping_time_i = ping_offset_i + sdr_start_time{1};
% 	gps_idx = abs(gps_data(:,1) - ping_time_i) < 0.5;
% 	gps_data_i = gps_data(gps_idx,:);
	
% 	gps_x = [gps_x; gps_data_i(2)];
% 	gps_y = [gps_y; gps_data_i(3)];
% 	gps_v_i = 10 * log10(abs(gps_v_raw));
% 	gps_t = [gps_t; min(gps_data_i(1))];
% 	gps_v = [gps_v; gps_v_i];
% end
% % clear i gps_v_i gps_data_i ping_time_i ping_offset_i max_sample_idx min_sample_idx;
% scatter(t_out(round((gps_t - gps_start) * OUTPUT_SAMPLE_RATE)), 10 * log10(abs(output_signal(round((gps_t - gps_start) * OUTPUT_SAMPLE_RATE)))));

% output_filename = sprintf('%s/fft_out.csv', ofile);
% dlmwrite(output_filename, [gps_t, gps_x, gps_y, gps_v, zeros(length(gps_t), 1)], 'precision', '%.3f')

% ping_timing = ping_starts - ping_starts(1);
% ping_indexes = round(ping_timing / period);
% offset = 0;
% candidate_length = round(0.02 * OUTPUT_SAMPLE_RATE + period * 0.1);
% new_pings = [];
% for i = 0:max(ping_indexes)
% 	if not(any(ping_indexes == i))
% 		% ping not found, find candidate
% 		last_ping = max(ping_indexes(ping_indexes <= i));
% 		possible_start = (ping_starts(find(ping_indexes == last_ping)) + period * (i - last_ping));
% 		candidate_start = round(possible_start - period * 0.05);
% 		candidate_signal = output_signal(candidate_start:candidate_start + candidate_length);
% 		% candidate_signal = getOriginalSignal(run_dir, run_num, candidate_start / OUTPUT_SAMPLE_RATE, candidate_length / OUTPUT_SAMPLE_RATE, SAMPLE_RATE);
% 		% line([candidate_start / OUTPUT_SAMPLE_RATE, candidate_start / OUTPUT_SAMPLE_RATE], ylim);
% 		% line([(candidate_start + candidate_length) / OUTPUT_SAMPLE_RATE, (candidate_start + candidate_length) / OUTPUT_SAMPLE_RATE], ylim);
% 		% lags = [];
% 		% rs = [];
% 		for j = 1:length(ping_starts)
% 		% 	start_time = ping_starts(j);
% 		% 	% template = output_signal(start_time - round(0.005 * OUTPUT_SAMPLE_RATE): start_time + round(0.030 * OUTPUT_SAMPLE_RATE));
% 		% 	template = getOriginalSignal(run_dir, run_num, (start_time - round(0.005 * OUTPUT_SAMPLE_RATE)) / OUTPUT_SAMPLE_RATE, 0.030, SAMPLE_RATE);
% 		% 	[r, lag] = xcorr(candidate_signal, template);
% 		% 	[max_r, max_ind] = max(abs(r));
% 		% 	lags = [lags, lag(max_ind)];
% 		% 	rs = [rs, max_r];
% 		% 	% figure;
% 		% 	% plot(lag(round(length(r) / 2):length(r)) / OUTPUT_SAMPLE_RATE, abs(r(round(length(r) / 2):length(r))));
% 		% 	% hold on;
% 		% 	% refline(0, max_r);
% 		% 	% line([lag(max_ind) / OUTPUT_SAMPLE_RATE, lag(max_ind) / OUTPUT_SAMPLE_RATE], ylim);
% 		% 	% refline(0, mean(abs(r(round(length(r) / 2):length(r)))));
% 		% 	% refline(0, std(abs(r(round(length(r) / 2):length(r)))) + mean(abs(r(round(length(r) / 2):length(r)))));
% 		end
% 		% ping_location = median(lags) / FFT_LENGTH + candidate_start
% 		% new_pings = [new_pings; round(ping_location)];
% 	end
% 	if i == 6
% 		% break
% 	end
% 	% close all;
% end
% % scatter(t_out(new_pings), 10 * log10(abs(output_signal(new_pings))));