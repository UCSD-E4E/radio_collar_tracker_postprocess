close all;
clear all;

threshold_history = csvread('/home/ntlhui/workspace/radio_collar_tracker_drone/tests/sdr_record/classifier_threshold.log');
data_in = csvread('/home/ntlhui/workspace/radio_collar_tracker_drone/tests/sdr_record/classifier_in.log');
% gps_data = csvread('/media/ntlhui/43C8-B1EA/2017.08.22/RUN_000055/GPS_000055');
signal_start_time_s = 1502770034.363384;
% gps_start_time_s = gps_data(1:1);
% local time, lat, lon, global time, alt, relative alt, vx, vy, vz, hdg
% lat = gps_data(:,2);
% lon = gps_data(:,3);
% gps_data_times = gps_data(:,1) - signal_start_time_s;
f_s = 2000000/6400;
time = 0:1/f_s:(length(data_in) - 1) / f_s;

static_offset = 1.5;

% recreation
% avg_len = floor(0.25*f_s)
% ping_len = ceil(0.02*f_s);
% peak_history = [ones(ping_len,1) * data_in(1); data_in];
% peak = zeros(length(data_in), 1);
% for k = 1:length(peak)
% 	peak(k) = max(peak_history(k:k+ping_len));
% end
% peak = [ones(avg_len,1) * peak(1); peak];
% peak_threshold = zeros(length(data_in), 1);
% for k = 1:length(peak_threshold)
% 	peak_threshold = median(peak(k:k+avg_len)) + 0.5;
% end

% peak_history = [ones(avg_len,1) * data_in(1); data_in];
% threshold = zeros(length(data_in),1);
% for k = 1:length(threshold)
% 	threshold(k) = mean(peak_history(k:k+avg_len)) + 1;
% end


figure;
subplot(2,1,1);
plot(time, data_in);
hold on;
grid on;
plot(time, threshold_history+1.5);
% plot(time, threshold);
% plot(time, peak_threshold);
lims = xlim;
% subplot(2,1,2);
% plot(gps_data_times, lat);
% hold on;
% grid on;
% yyaxis right;
% plot(gps_data_times, lon);
% xlim(lims);