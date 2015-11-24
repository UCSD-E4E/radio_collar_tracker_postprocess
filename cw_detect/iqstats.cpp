#include <unistd.h>
#include <cmath>
#include <getopt.h>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <cstdint>
#include <iomanip>
#include <fstream>

using namespace std;

enum DataType{
	UINT8,
	FLOAT
};

template <typename Type> void proc_file(ifstream* in_file);
template <> void proc_file <float> (ifstream* in_file);

int main(int argc, char** argv){
	int opt;
	DataType data_type = UINT8;
	while ((opt = getopt(argc, argv, "hf")) != -1){
		switch(opt){
			case 'h':
			case '?':
				exit(0);
			case 'f':
				data_type = FLOAT;
				break;
		}
	}
	cout << "Interpreting as ";
	switch(data_type){
		case FLOAT:
			cout << "float";
			break;
		case UINT8:
			cout << "uint8_t";
			break;
	}
	cout << endl;
	string input_file (argv[optind]);
	struct stat buffer;
	if (stat(input_file.c_str(), &buffer)){
		cerr << "Error: Could not stat file!" << endl;
		exit(-1);
	}
	if (!S_ISREG(buffer.st_mode)){
		cerr << "Error: Not a file!" << endl;
		exit(-1);
	}
	ifstream in_file;
	in_file.open(input_file, ios::in | ios::binary);
	if(in_file.bad()){
		cerr << "Error: Could not open file!" << endl;
		exit(-1);
	}

	switch(data_type){
		case UINT8:
			proc_file <uint8_t> (&in_file);
			break;
		case FLOAT:
			proc_file <float> (&in_file);
			break;
	}

	in_file.close();
	return 0;
}

template <typename Type> void proc_file(ifstream* in_file){
	Type buff = 0;
	uint32_t sample_counter = 0;
	float fbuff;
	double average = 0;
	double sq_sum = 0;
	double min = 1.0;
	double max = 0;
	float mag = 0;

	while(in_file->peek() != EOF){
		// Get the I byte
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(Type));
		fbuff = buff / 128.0 - 1.0;
		mag = fbuff * fbuff;
		
		// Get the Q byte
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(Type));
		fbuff = buff / 128.0 - 1.0;
		mag += fbuff * fbuff;
		mag = sqrt(mag);

		if(mag < min){
			min = mag;
		}
		if(mag > max){
			max = mag;
		}
		average += mag;
		sq_sum += mag * mag;
		sample_counter++;
	}
	average /= sample_counter;
	sq_sum = sq_sum / sample_counter - average * average;
	cout << "Average: " << average << endl;
	cout << "Std Dev: " << sqrt(sq_sum) << endl;
	cout << "Max: " << max << endl;
	cout << "Min: " << min << endl;
	cout << "Count: " << sample_counter << endl;
}

template <> void proc_file<float>(ifstream* in_file){
	float buff = 0;
	uint32_t sample_counter = 0;
	float fbuff;
	double average = 0;
	double sq_sum = 0;
	double min = 1.0;
	double max = 0;
	float mag = 0;

	while(in_file->peek() != EOF){
		// get I sample
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(float));
		fbuff = buff;
		mag = fbuff * fbuff;

		// get the Q sample
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(float));
		fbuff = buff;
		mag += fbuff * fbuff;
		mag = sqrt(mag);

		if(mag < min){
			min = mag;
		}
		if(mag > max){
			max = mag;
		}
		average += mag;
		sq_sum += mag * mag;
		sample_counter ++;
	}
	average /= sample_counter;
	sq_sum = sq_sum / sample_counter - average * average;
	cout << "Average: " << average << endl;
	cout << "Std Dev: " << sqrt(sq_sum) << endl;
	cout << "Max: " << max << endl;
	cout << "Min: " << min << endl;
	cout << "Count: " << sample_counter << endl;
}
