clear all
% close all

FFT_LENGTH = 4096;
SAMPLE_RATE = 2000000;
OUTPUT_SAMPLE_RATE = SAMPLE_RATE / FFT_LENGTH;
SIG_LENGTH = int16(0.015 * SAMPLE_RATE / FFT_LENGTH);
collar_Freq = 172950873;

run_dir = '/home/ntlhui/workspace/2017.07.06.RCT_Test/RUN_000003';
ofile = '/tmp/sdr_data';
freq_bin = round((collar_Freq - center_freq) / SAMPLE_RATE * FFT_LENGTH);
run_num = 4;

raw_files = dir([run_dir, '/RAW_DATA_*']);

output_signal = [];
leftovers = [];

for file_idx = 1:min(5, length(raw_files))
	data = [leftovers; raw2complex(fullfile(raw_files(file_idx).folder, raw_files(file_idx).name))];
	for start_idx = 1:FFT_LENGTH:length(data)
		fft_buffer_in = data(start_idx:start_idx + FFT_LENGTH - 1);
		fft_buffer_out = fft(fft_buffer_in);
		% fft_buffer_out = [fft_buffer_out(FFT_LENGTH / 2 + 1 : FFT_LENGTH) fft_buffer_out(1:FFT_LENGTH / 2)];
		output_signal = [output_signal; (fft_buffer_out(freq_bin))];
	end
	leftovers = data(start_idx + FFT_LENGTH:length(data));
end

figure;

% plotting the filtered signal
plot(1/OUTPUT_SAMPLE_RATE:1/OUTPUT_SAMPLE_RATE:length(output_signal)/OUTPUT_SAMPLE_RATE, 10 * log10(abs(output_signal)))
hold on;
collar_candidate = [];
for i = 1 : int64(2 * OUTPUT_SAMPLE_RATE) : int64(length(output_signal) / int64(2 * OUTPUT_SAMPLE_RATE)) * int64(2 * OUTPUT_SAMPLE_RATE)
	collar_candidate = [collar_candidate; max(abs(output_signal(i:i+int64(2 * OUTPUT_SAMPLE_RATE) - 1)))];
end

% Plot the collar candidate threshold
% plot(1:2:length(collar_candidate) * 2 - 1, 10 * log10(abs(collar_candidate)));

% Generate the histogram based threshold
[counts, edges] = histcounts(10 * log10(abs(collar_candidate)), 15);
count_threshold = 0;
for i = length(counts):-1:1
	if counts(i) > mean(counts)
		count_threshold = edges(i + 1);
		break
	end
end
refline(0, count_threshold);

% Find pings based on histogram threshold
ping_times = find(10 * log10(abs(output_signal)) > count_threshold);
ping_starts = [ping_times(1)]; % in OUTPUT_SAMPLE_RATE
for i = 1:length(ping_times) - 1
	if ping_times(i + 1) - ping_times(i) > 1
		ping_starts = [ping_starts; ping_times(i + 1)];
	end
end

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
disp(ping_lengths);

% Get frequency of pings
ping_frequencies = [];
for i = 1:length(ping_starts)
	start_time = ping_starts(i) / OUTPUT_SAMPLE_RATE;
	ping_signal = getOriginalSignal(run_dir, run_num, start_time, 0.010, SAMPLE_RATE);
	guess = 172951000;
	freq = getFrequencyOfPing(ping_signal, SAMPLE_RATE, guess);
	ping_frequencies = [ping_frequencies; freq];
end
probable_frequency = int64(median(ping_frequencies));

% Get periods of pings
periods = []; %in OUTPUT_SAMPLE_RATE
for i = 1:length(ping_starts) - 1
	periods = [periods; ping_starts(i + 1) - ping_starts(i)];
end
median_period = median(periods);
periods = periods(periods < 1.1 * median_period);
periods = periods(periods > 0.9 * median_period);
period = mean(periods);

% Circle all known pings
t_out = 1/OUTPUT_SAMPLE_RATE:1/OUTPUT_SAMPLE_RATE:length(output_signal) / OUTPUT_SAMPLE_RATE;
scatter(t_out(ping_starts), 10 * log10(abs(output_signal(ping_starts))));

ping_timing = ping_starts - ping_starts(1);
ping_indexes = round(ping_timing / period);
offset = 0;
candidate_length = round(0.02 * OUTPUT_SAMPLE_RATE + period * 0.1);
new_pings = [];
for i = 0:max(ping_indexes)
	if not(any(ping_indexes == i))
		% ping not found, find candidate
		last_ping = max(ping_indexes(ping_indexes <= i));
		possible_start = (ping_starts(find(ping_indexes == last_ping)) + period * (i - last_ping));
		candidate_start = round(possible_start - period * 0.05);
		% candidate_signal = output_signal(candidate_start:candidate_start + candidate_length);
		% candidate_signal = getOriginalSignal(run_dir, run_num, candidate_start / OUTPUT_SAMPLE_RATE, candidate_length / OUTPUT_SAMPLE_RATE, SAMPLE_RATE);
		line([candidate_start / OUTPUT_SAMPLE_RATE, candidate_start / OUTPUT_SAMPLE_RATE], ylim);
		line([(candidate_start + candidate_length) / OUTPUT_SAMPLE_RATE, (candidate_start + candidate_length) / OUTPUT_SAMPLE_RATE], ylim);
		lags = [];
		rs = [];
		% for j = 1:length(ping_starts)
		% 	start_time = ping_starts(j);
		% 	% template = output_signal(start_time - round(0.005 * OUTPUT_SAMPLE_RATE): start_time + round(0.030 * OUTPUT_SAMPLE_RATE));
		% 	template = getOriginalSignal(run_dir, run_num, (start_time - round(0.005 * OUTPUT_SAMPLE_RATE)) / OUTPUT_SAMPLE_RATE, 0.030, SAMPLE_RATE);
		% 	[r, lag] = xcorr(candidate_signal, template);
		% 	[max_r, max_ind] = max(abs(r));
		% 	lags = [lags, lag(max_ind)];
		% 	rs = [rs, max_r];
		% 	% figure;
		% 	% plot(lag(round(length(r) / 2):length(r)) / OUTPUT_SAMPLE_RATE, abs(r(round(length(r) / 2):length(r))));
		% 	% hold on;
		% 	% refline(0, max_r);
		% 	% line([lag(max_ind) / OUTPUT_SAMPLE_RATE, lag(max_ind) / OUTPUT_SAMPLE_RATE], ylim);
		% 	% refline(0, mean(abs(r(round(length(r) / 2):length(r)))));
		% 	% refline(0, std(abs(r(round(length(r) / 2):length(r)))) + mean(abs(r(round(length(r) / 2):length(r)))));
		% end
		% ping_location = median(lags) / FFT_LENGTH + candidate_start
		% new_pings = [new_pings; round(ping_location)];
	end
	if i == 6
		% break
	end
	% close all;
end
% scatter(t_out(new_pings), 10 * log10(abs(output_signal(new_pings))));