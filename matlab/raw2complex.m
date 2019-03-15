function [data] = raw2complex(filename)
%RAW2COMPLEX converts a raw binary file consisting of 8 bit real/imag
%values

fileID = fopen(filename);
bin = fread(fileID, 'int16');

data_length = length(bin);

reals = bin(1:2:data_length)/4096.0;
imags = bin(2:2:data_length)/4096.0;

data = complex(reals, imags);

fclose(fileID);

end

