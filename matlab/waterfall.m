%% waterfall: Creates a waterfall plot of the input file
function [] = waterfall(file, minY, maxY)
	FFT_LEN = 4096;
	CENTER_FREQ = 172500000;
	data = raw2complex(file);

	data_len = length(data);
	num_ffts = floor(data_len / FFT_LEN);
	fft_in_data = reshape(data(1:num_ffts * FFT_LEN), [FFT_LEN, num_ffts]);
	fft_out_data = fft(fft_in_data);
	fft_out_data = fftshift(fft_out_data);
	P2 = abs(fft_out_data / FFT_LEN);
	% P2 = [P2(FFT_LEN/2+1:FFT_LEN,:); P2(1:FFT_LEN/2,:)];
	waterfall_plot = 10*log10(abs(P2))';
	figure('units','normalized','outerposition',[0 0 1 1]);
	% imagesc(x, y, C)
	y = [(CENTER_FREQ - 1e6) / 1e6, (CENTER_FREQ + 1e6) / 1e6];
	% x = [1,FFT_LEN/2];
	x = [0, data_len / 2000000];
	C = waterfall_plot(:,1:FFT_LEN)';
	clims = [max(std(waterfall_plot)) + mean(mean(waterfall_plot)), max(max(waterfall_plot))];
	clims = [mean(mean(waterfall_plot)), max(max(waterfall_plot))];
	imagesc(x, y, C, clims);
	c = colorbar;
	c.Label.String = 'Signal Strength (dBFS)';
	xlabel('Time (s)');
	ylabel('Frequency (MHz)');
	title('Signal Waterfall Plot');
	ylim_old = ylim;
	set(gca, 'ylim', [minY, maxY]);