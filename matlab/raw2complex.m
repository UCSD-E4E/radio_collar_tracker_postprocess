function [data] = raw2complex(filename)
%RAW2COMPLEX converts a raw binary file consisting of 8 bit real/imag
%values

fileID = fopen(filename);
% bin = fread(fileID, 'uint8');
bin = fread(fileID, 'int16');

length = size(bin, 1);

% real = bin(1:2:length)/128.0 - 1;
% imag = bin(2:2:length)/128.0 - 1;

real = bin(1:2:length)/4096.0;
imag = bin(2:2:length)/4096.0;

data = complex(real, imag);

fclose(fileID);

end

