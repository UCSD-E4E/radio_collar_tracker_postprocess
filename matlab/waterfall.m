close all;
clear all;

FFT_LEN = 4096;
CENTER_FREQ = 172250000;
data = raw2complex('/tmp/sdr_data/RAW_DATA_000001_000001');

data_len = length(data);
num_ffts = data_len / FFT_LEN;
fft_in_data = reshape(data, [FFT_LEN, num_ffts]);
fft_out_data = fft(fft_in_data);
P2 = abs(fft_out_data / FFT_LEN);
P2 = [P2(FFT_LEN/2+1:FFT_LEN,:); P2(1:FFT_LEN/2,:)];
waterfall_plot = 10*log10(abs(P2))';
figure;
imagesc([(0 + CENTER_FREQ) / 1e6, (1e6 + CENTER_FREQ) / 1e6], [0, data_len / 2000000], waterfall_plot(:,FFT_LEN/2+1:FFT_LEN), [max(std(waterfall_plot)) + mean(mean(waterfall_plot)), max(max(waterfall_plot))]);
c = colorbar;
c.Label.String = 'Signal Strength (dBFS)'
ylabel('Time (s)');
xlabel('Frequency (MHz)');
title('Signal Waterfall Plot');