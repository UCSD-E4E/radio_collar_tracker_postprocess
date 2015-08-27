#include <unistd.h>
#include <getopt.h>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <cstdint>
#include <iomanip>
#include <fstream>
#include <cmath>

using namespace std;

enum DataType{
	UINT8,
	FLOAT
};

template <typename Type> void proc_file (ifstream* infile);
template <> void proc_file <float> (ifstream* in_file);
template <> void proc_file <uint8_t> (ifstream* in_file);

int main(int argc, char** argv){
	int opt;
	DataType data_type = FLOAT;
	while ((opt = getopt(argc, argv, "hb")) != -1){
		switch(opt){
			case 'h':
			case '?':
			default:
				exit(0);
			case 'b':
				data_type = UINT8;
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
		case FLOAT:
			proc_file <float> (&in_file);
			break;
		case UINT8:
			proc_file <uint8_t> (&in_file);
			break;
	}

	in_file.close();
	return 0;
}

template <> void proc_file <float> (ifstream* in_file){
	float buff[2];
	uint32_t sample_counter = 0;
	float mag = 0;
	while(in_file->peek() != EOF){
		// get I sample
		in_file->read(reinterpret_cast <char*> (&buff), 2 * sizeof(float));
		cout << setw(9) << sample_counter << ":\t";
		cout << setw(9) << fixed << setprecision(7);
		mag = sqrt(buff[0] * buff[0] + buff[1] * buff[1]);
		cout << mag << endl;
		sample_counter++;

	}
}

template <> void proc_file <uint8_t> (ifstream* in_file){
	uint8_t buff[2];
	uint32_t sample_counter = 0;
	float mag = 0;
	float fbuff[2];
	while(in_file->peek() != EOF){
		// get I sample
		in_file->read(reinterpret_cast <char*> (&buff), 2 * sizeof(uint8_t));
		fbuff[0] = buff[0] / 128.0 - 1.0;
		fbuff[1] = buff[1] / 128.0 - 1.0;
		cout << setw(9) << sample_counter << ":\t";
		cout << setw(9) << fixed << setprecision(7);
		mag = sqrt(fbuff[0] * fbuff[0] + fbuff[1] * fbuff[1]);
		cout << mag << endl;
		sample_counter++;
	}
}

