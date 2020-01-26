function waterfall(fft_len, center_freq, samp_freq, data)
	data_len = length(data);
	num_ffts = floor(data_len / fft_len);
	fft_in_data = reshape(data(1:num_ffts * fft_len), [fft_len, num_ffts]);
	fft_out_data = fft(fft_in_data);
	shifted_amp_data = abs(fft_out_data / fft_len);
	% amp_data = [shifted_amp_data(fft_len / 2 + 1 : fft_len, :); ...
	% 	shifted_amp_data(1 : fft_len / 2, :)];
	power_data = fftshift(10 * log10(abs(shifted_amp_data))',2);
	fig = figure;
	freq_bound = samp_freq / 2;
	imagesc([(-freq_bound + center_freq) / 1e6, (freq_bound + center_freq) / 1e6], ...
		[0, data_len / samp_freq], power_data, ...
		[mean(std(power_data)) + mean(mean(power_data)), max(max(power_data))]);
	c = colorbar;
	c.Label.String = 'Signal Strength (dBFS)';
	ylabel('Time (s)');
	xlabel('Frequency (MHz)');
	title('Signal Waterfall Plot');
