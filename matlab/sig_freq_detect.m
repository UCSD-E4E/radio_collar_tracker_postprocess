%{
This program is effective for comparing 60ms sample data to 60ms template.
If some other time amount is used the execution time will vary. Please
check xcorr() documentation if this is required. The value to be
manipulated is called 'xcorr_len'.

To run this program using file data instead of a self-made sample, comment
out block labeled 'Self-made Sample Block' and comment in blocks labeled
'Initialization Block', 'File Load Block' and 'Choose Sample Block'.

NOTES:
Limitation is -34dB.

If using any other program during execution, perfomance will be effected.

MAXVals is not maximum values.
%}

SAMPLING_RATE = 2048000; %samples per second

%{
Initialization Block:
This block initializes necessary variables for file usage and computation.
%}
%{
% Change file directory. There 3 other places where this needs to be done.
file = '/Users/JacobDomine/Desktop/RUN_010008/RAW_DATA_010008_00000';

TIME_PER_SAMPLE = 1/SAMPLING_RATE; %seconds per sample
SAMPLE_WINDOW = 0.06;    % 60ms sample window
SAMPLE_SIZE = SAMPLE_WINDOW*SAMPLING_RATE;
sum = 0;                 % Total samples in all data files.
b = zeros(40,1);         % Used to calculate sum
y = zeros(SAMPLE_SIZE,1); 
%}

%{
122880 is the number of samples for 60ms.
Manipulating this value will alter the time of the sample data.
%}

sigfreq = 4000;       % Approximate frequency of signal 
PING_LEN = 0.060;
xcorr_len = int16(PING_LEN * SAMPLING_RATE);         % 60ms xcorr. Length of cross correlation
lenFreqs = 0;           % Length of Freqs array
lenMAXVals = 0;         % Length of MAXVals array
deviation = 5000;       % Frequency deviation check sigfreq +/- deviation
meanV = 0;              % Mean value of MAXVals
stdV = 0;               % Standard deviation of MAXVals

%{
File Load Block:
This block of code gets the total number of samples in the data
files (sum) and loads every sample into an array (full).
%}
%{
for i = 1:40
    if i == 10
        % Change file directory
        file = '/Users/JacobDomine/Desktop/RUN_010008/RAW_DATA_010008_0000';
    end
    itoa = strcat(file,num2str(i));
    disp(itoa);
    a = raw2complex(itoa); 
    b(i) = length(a);
    sum = sum + length(a);
end
full = zeros(sum,1);
% Change file directory
file = '/Users/JacobDomine/Desktop/RUN_010008/RAW_DATA_010008_00000';
for i = 1:40
    if i == 10
        % Change file directory
        file = '/Users/JacobDomine/Desktop/RUN_010008/RAW_DATA_010008_0000';
    end
    itoa = strcat(file,num2str(i));
    disp(itoa);
    a = raw2complex(itoa); 
    full(b(i)*i-b(i)+1:b(i)*i) = a(1:length(a));
end

% Holds the time of each sample starting from time = TIME_PER_SAMPLE 
t = TIME_PER_SAMPLE:TIME_PER_SAMPLE:TIME_PER_SAMPLE*length(full);
s = 1:length(full);
%}

%{
Choose Sample Block:
This block will allow you to select a time to start the sample and
automatically get the sample array and load it into array 'sample'.
%}
%{
prompt = 'Please enter beginning time of sample:';
start = input(prompt)
for i = 1:length(s)
    if start == t(i)
        initial = i;
        break
    end
end
for i = initial:initial+SAMPLE_SIZE
    y(i-initial+1) = full(i);
end
%}

%{
Self-made Sample Block:
This block of code creates a 2.06 second signal at a particular angular
frequency and stores it in the variable y. 
y holds 2 -- 60ms pulses and 0 for all other values.
y is then altered by adding in a certain amount of noise using awgn().
%}
f1 = 5000;
sig_len = 2.06;
w1 = 2*pi*f1;
len = 0:1/SAMPLING_RATE:sig_len;
y = complex(zeros(length(len),1));
for i = 1:1/SAMPLING_RATE:1+PING_LEN
    y(int32(i*SAMPLING_RATE+1)) = cos(w1*i) + j * sin(w1*i);
end
y = awgn(y,10);

%{
Initializes 2 arrays and sets up the the snr test sequence 0 dB ---> -40 dB

MAXVals: holds the Mean of the Absolute value of the cross correlation (Xcorr) at a
         given frequency. This isn't the Maximum values but rather the
         Mean(Abs(Xcorr())) of the sample signal with the template

Freqs:   holds the frequency being tested in the cross correlation
%}
MAXVals = zeros(1,1);
Freqs = 1:length(MAXVals);
lmsnr = [0 -3];

%{
Main computational block

(1) Using the values of log magnitude of snr calculate the actual snr. 

(2) From experimentation the incrementation value can be calculated by 
    using the best fit line from observed data. 
    FInc: Frequency Incrementation

(3) Begin cross correlating frequencies between 
    (approximate frequency) - 5kHz and (approximate frequency) + 5kHz. If
    the (approximate frequency) is less than or equal to 5kHz the template 
    will start at 1Hz.The result of computation is held in MAXVals and the 
    frequency tested is held in Freqs.
    x is the template. y is the sample signal.

Note: 1 and 2 will be used later too but this initial usage is used to get
      the average value of the MAXVals array which will help in estimating
      the SNR.

(4) Calculates the mean value of the current MAXVals array. This block also
    estimates the SNR using a best fit equation found using a self-made 
    test signal.

(5) Gets the total number of elements of Freqs and MAXVals. Used to add 
    new elements to the end of MAXVals and Freqs.

(6) Redo processes 1 and 2 using the estimated SNR. Computes cross
    correlation using the new incrementation value FInc. The estimated SNR
    will always get a valid FInc within the design parameters of this
    program (0dB to -34dB)

(7) Using the maximum value in MAXVals check half way in between the
    adjacent elements and determine which is greater and take that as the
    new maximum. Doing this 12 times allows for accurate frequency
    determination.

(8) Check to see if the maximum value in MAXVals is statistically
    significant.
%}
for j = 1:2
    % (1)
    snr = 10^(lmsnr(j)/20);
    
    % (2)
    FInc = 320*snr;                
    
    % (3)
    for i = sigfreq-deviation:FInc:sigfreq+deviation
        f = i;
        w = 2*pi*f;
        for template = 0:1/SAMPLING_RATE:PING_LEN
            x(int32(template*SAMPLING_RATE+1)) = cos(w*template) + j * sin(w*template);
        end
        
        r = xcorr(y,x,xcorr_len); 
        
        Freqs(int32(((i-sigfreq+5000)/FInc)+1)+lenFreqs) = f;
        MAXVals(int32(((i-sigfreq+5000)/FInc)+1)+lenMAXVals) = mean(abs(r));
    end
   
    %(4)
    meanV = mean(MAXVals);
    estimatesnr = log(meanV/250)/(-0.09);
    
    %(5)
    lenFreqs = length(Freqs);
    lenMAXVals = length(MAXVals);
end

%{
Execution Time Estimation Block:
Estimates the total execution time of the program. Helpful for my usage to  
estimate the amount of time the program will execute for. However, 
depending on the technology being used this time may vary.
%}
%{
if lt(estimatesnr,-25)
    disp('Very Slow: 15+ minutes')
elseif lt(estimatesnr,-15)
    disp('Slow: 10-15 minutes')
elseif lt(estimatesnr,-5)
    disp('Average: 5-10 minutes')
else
    disp('Fast: 2-5 minutes')
end
%}

%(6)    
snr = 10^(estimatesnr/20);
FInc = 320*snr;
if lt(estimatesnr,-5)
    for i = sigfreq-deviation:FInc:sigfreq+deviation
        f = i;
        w = 2*pi*f;
        for template = 0:1/SAMPLING_RATE:PING_LEN
            x(int32(template*SAMPLING_RATE+1)) = cos(w*template) + j * sin(w*template);
        end

        r = xcorr(y,x,xcorr_len); 

        Freqs(int32(((i-sigfreq+5000)/FInc)+1)+lenFreqs) = f;
        MAXVals(int32(((i-sigfreq+5000)/FInc)+1)+lenMAXVals) = mean(abs(r));
    end
end

%(8)
meanV = mean(MAXVals);
stdV = std(MAXVals);

%(7)
for iteration = 1:12
    it = 2^iteration;
    [M,I] = max(MAXVals);
    %sprintf('%10.3f',Freqs(I))
    maxF = Freqs(I);
    for i = length(MAXVals):-1:I+1
        MAXVals(i+2) = MAXVals(i);
        Freqs(i+2) = Freqs(i);
    end
    MAXVals(I+1) = MAXVals(I);
    Freqs(I+1) = Freqs(I);
    for i = -1:2:1
        f = maxF + (i*FInc)/it;
        Freqs(I+1+i) = f;
        w = 2*pi*f;
        for template = 0:1/SAMPLING_RATE:PING_LEN
            x(int32(template*SAMPLING_RATE+1)) = cos(w*template) + j * sin(w*template);
        end
        r = xcorr(y,x,xcorr_len);
        MAXVals(I+1+i) = mean(abs(r));
    end
end

%(8)
if lt(MAXVals(I),meanV+3*stdV)
    disp('Best Guess: ');
end

%{
Print out final frequency value.

Plot Freqs vs. MAXVals.

Create a reference line that shows the threshold to being statistically
significant.
%}
figure;
sprintf('%10.3f',Freqs(I))
scatter(Freqs,MAXVals);
ref = refline([0 meanV]);
ref.Color = 'r';
