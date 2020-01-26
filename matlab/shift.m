function [signal] = shift(input_signal, shift_amt, sampling_freq)
	signal_length = length(input_signal) / sampling_freq;
	t = 0:1/sampling_freq:signal_length - 1/sampling_freq;
	mixing_signal = cos(-2 * pi * shift_amt * t) + i * sin(-2 * pi * shift_amt * t);
	mixing_signal = mixing_signal(:);
	input_signal = input_signal(:);
	signal = input_signal .* mixing_signal;
end