clear all;
close all;

run_num = 55;
files = 41;
data_dir = sprintf("/media/ntlhui/43C8-B1EA/2017.08.22/RUN_%06d", run_num);
% data_dir = "/home/ntlhui/workspace/tmp/testData/";
f_s = 2000000;

ignore = mkdir(sprintf("RUN_%06d", run_num));

int_len = 6400;

final_freq = f_s / int_len;
start_idx = 0;

threshold = 100;
for i = 1:files
	data = raw2complex(sprintf("%s/RAW_DATA_%06d_%06d", data_dir, run_num, i));
	mag_data = abs(data).^2;
	% integrated_data = mag_data;
	integrated_data = zeros(floor(length(data) / int_len), 1);
	for j = 1:length(integrated_data)
		integrated_data(j) = sum(mag_data((j - 1) * int_len + 1 : j * int_len - 1));
	end
	log_data = 20 * log10(integrated_data);

	if threshold == 100
		threshold = log_data(1);
	end

	time = start_idx / final_freq : 1 / final_freq : (start_idx + length(log_data) - 1) / final_freq;

	plot(time, log_data);
	saveas(gcf, sprintf("RUN_%06d/RAW_DATA_%06d_%06d.fig", run_num, run_num, i));
	start_idx = start_idx + length(log_data);
end

close;