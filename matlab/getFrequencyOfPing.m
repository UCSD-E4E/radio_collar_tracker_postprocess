%% getFrequencyOfPing: pass in 5 ms only!
function [frequency] = getFrequencyOfPing(signal, sampling_frequency, guess)
	f_dev = 10000;
	fft_out = fft(signal);
	P2 = abs(fft_out / length(signal));
	P2 = fftshift(P2);
	waterfall_plot = 10*log10(abs(P2))';
	% figure;
	% plot(-sampling_frequency / 2 + 172500000:sampling_frequency/(length(signal) - 1):sampling_frequency / 2 + 172500000, waterfall_plot)
	% % plot(waterfall_plot)
	% refline(0, max(waterfall_plot));
	% grid on;

	bin_width = sampling_frequency / length(waterfall_plot);
	bin_number = floor((guess - 172500000) / bin_width) + length(waterfall_plot) / 2;
	f_dev_bin = ceil(f_dev / bin_width);
	f_max = bin_number + f_dev_bin;
	f_min = bin_number - f_dev_bin;
	if f_min < 1
		f_min = 1;
	end
	if f_max > length(waterfall_plot)
		f_max = length(waterfall_plot);
	end
	[val, frequency_ind] = max(waterfall_plot(f_min:f_max));
	frequencies = (-sampling_frequency / 2 + 172500000:sampling_frequency/(length(signal) - 1):sampling_frequency / 2 + 172500000);
	frequency = frequencies(frequency_ind + f_min);
	
	% xcorr test

	% TEMPLATE_LEN = length(signal) / 4 / sampling_frequency;
	% f_dev = 1000;
	% f_inc = 100;
	% t = 1/sampling_frequency:1/sampling_frequency:TEMPLATE_LEN / sampling_frequency;
	% f_xcorr = [];
	% f_test = [];
	% for f = frequency - f_dev:f_inc:frequency+f_dev
	% 	f_test = [f_test; f];
	% 	template = 0.5*(cos(2 * pi * f * t) + j * sin(2 * pi * f * t));
	% 	[r, lags] = xcorr(signal, template);
	% 	f_xcorr = [f_xcorr; mean(abs(r))];
	% end
	% % [val, frequency_ind] = max(f_xcorr);
	% % frequency = f_test(frequency_ind);

	% figure;
	% plot(f_test, f_xcorr);
	% hold on;
	% line([frequency, frequency], ylim);
	% refline(0, max(f_xcorr));