close all;
clear all;

SIG_LEN = 0.5;
PING_LEN = 0.060;
TEMPLATE_LEN = PING_LEN;
SAMPLING_RATE = 2000000;
f1 = 50000;
start_time = 0.2;
signal = complex(zeros(SIG_LEN * SAMPLING_RATE, 1));
for t = start_time + 1/SAMPLING_RATE:1/SAMPLING_RATE:start_time + PING_LEN
	signal(int64(t * SAMPLING_RATE)) = 0.01 * (cos(2 * pi * f1 * t) + j * sin(2 * pi * f1 * t));
end
sig_power = bandpower(signal(int64((start_time + 1/SAMPLING_RATE) * SAMPLING_RATE):int64((start_time + PING_LEN) * SAMPLING_RATE)))
signal = awgn(signal, -30, 'measured');

t = 1/SAMPLING_RATE:1/SAMPLING_RATE:TEMPLATE_LEN;
f2_center = 50000;
f_dev = 1500;
f_inc = 50;
frequencies = [];
xcorr_vals = [];
for f2 = f2_center - f_dev : f_inc : f2_center + f_dev
	template = 0.5*(cos(2 * pi * f2 * t) + j * sin(2 * pi * f2 * t));
	[r, lags] = xcorr(signal, template);
	frequencies = [frequencies; f2];
	xcorr_vals = [xcorr_vals; max(abs(r))];
end
figure;
scatter(f2_center - frequencies, xcorr_vals);
set(gca,'yscale','log')
hold on;
grid on;
refline(0, mean(xcorr_vals));
refline(0, mean(xcorr_vals) + std(xcorr_vals));
refline(0, mean(xcorr_vals) - std(xcorr_vals));

figure;
plot(1/SAMPLING_RATE:1/SAMPLING_RATE:SIG_LEN, real(signal));

FFT_LEN = 4096;
CENTER_FREQ = 0;

data_len = length(signal);
num_ffts = data_len / FFT_LEN;
fft_in_data = reshape(signal(1:floor(num_ffts) * FFT_LEN), [FFT_LEN, floor(num_ffts)]);
fft_out_data = fft(fft_in_data);
P2 = abs(fft_out_data / FFT_LEN);
P2 = [P2(FFT_LEN/2+1:FFT_LEN,:); P2(1:FFT_LEN/2,:)];
waterfall_plot = 10*log10(abs(P2))';
figure;
% imagesc(x, y, C)
x = [(0 + CENTER_FREQ) / 1e6, (1e6 + CENTER_FREQ) / 1e6];
y = [0, data_len / SAMPLING_RATE];
C = waterfall_plot(:,FFT_LEN/2+1:FFT_LEN);
clims = [max(std(waterfall_plot)) + mean(mean(waterfall_plot)), max(max(waterfall_plot))];
imagesc(x, y, C, clims);
c = colorbar;
c.Label.String = 'Signal Strength (dBFS)';
ylabel('Time (s)');
xlabel('Frequency (MHz)');
title('Signal Waterfall Plot');