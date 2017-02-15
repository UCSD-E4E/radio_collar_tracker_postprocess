function [ data, length ] = raw2complex(filename)
%RAW2COMPLEX converts a raw binary file consisting of 8 bit real/imag
%values

fileID = fopen(filename);
bin = fread(fileID, 'uint8');

length = size(bin, 1);

real = bin(1:2:length) - 128;
imag = bin(2:2:length) - 128;

data = complex(real, imag);

fclose(fileID);

end

