close all;
clear all;

center_frequency = 173500000;
sampling_frequency = 2000000;
target_frequency = 173763000;
filter_frequency = 500;
upsample_ratio = 1;
downsample_ratio = 200;
num_taps = 100;


% get data
data = raw2complex('/home/ntlhui/workspace/tmp/testData/RAW_DATA_000001_000001');
tic
signal_length = length(data) / sampling_frequency;
shifted_signal = shift(data, target_frequency - (center_frequency + ...
	filter_frequency), sampling_frequency);
resampled_signal = resample(shifted_signal', upsample_ratio, downsample_ratio);
match_output = match(resampled_signal, filter_frequency, num_taps, ...
	sampling_frequency);
resampled_t = 0:1 / (sampling_frequency / downsample_ratio) : 1 / (sampling_frequency / downsample_ratio) * (length(match_output) - 1);
mean_output = mean(match_output);
var_output = var(match_output);
bound = mean_output + 3 * sqrt(var_output);
toc
plot(resampled_t, match_output);
hold on;
plot([0 max(resampled_t)], [bound bound]);
plot([0 max(resampled_t)], [mean_output mean_output]);
