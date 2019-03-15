close all;
clear all;

fft_len = 2048;
center_freq = 172500000;
samp_freq = 2000000;
start_time = 0;
for i = 1:1
	data = raw2complex(sprintf('/home/ntlhui/workspace/tmp/testData/RAW_DATA_000001_%06d',i));

	data_len = length(data);
	num_ffts = floor(data_len / fft_len);
	fft_in_data = reshape(data(1:num_ffts * fft_len), [fft_len, num_ffts]);
	fft_out_data = fft(fft_in_data);
	P2 = abs(fft_out_data / fft_len);
	amp_data = [P2(fft_len/2+1:fft_len,:); P2(1:fft_len/2,:)];
	waterfall_plot = fftshift(10*log10(abs(amp_data))',2);
	figure;
	imagesc([(-1e6 + center_freq) / 1e6, (1e6 + center_freq) / 1e6], ...
		[start_time, start_time + data_len / samp_freq], ...
		waterfall_plot, ...
		[max(std(waterfall_plot)) + mean(mean(waterfall_plot)), ...
		max(max(waterfall_plot))]);
	c = colorbar;
	c.Label.String = 'Signal Strength (dBFS)';
	ylabel('Time (s)');
	xlabel('Frequency (MHz)');
	title('Signal Waterfall Plot');
	% saveas(gcf, sprintf('RUN_000014_%06d', i));
	% close;
	start_time = start_time + data_len / samp_freq;
end