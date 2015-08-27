#include <unistd.h>
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

	while(in_file->peek() != EOF){
		// Get the I byte
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(Type));
		fbuff = buff / 128.0 - 1.0;
		cout << setw(9) << sample_counter << ":\t";
		cout << setw(9) << fixed << setprecision(7);
		cout << fbuff << "\t";
		
		// Get the Q byte
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(Type));
		fbuff = buff / 128.0 - 1.0;
		cout << setw(9) << fixed << setprecision(7);
		cout << fbuff << endl;
		sample_counter++;
	}
}

template <> void proc_file<float>(ifstream* in_file){
	float buff = 0;
	uint32_t sample_counter = 0;
	while(in_file->peek() != EOF){
		// get I sample
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(float));
		cout << setw(9) << sample_counter << ":\t";
		cout << setw(9) << fixed << setprecision(7);
		cout << buff << "\t";

		// get the Q sample
		in_file->read(reinterpret_cast <char*> (&buff), sizeof(float));
		cout << setw(9) << fixed << setprecision(7);
		cout << buff << endl;
		sample_counter++;
	}
}
