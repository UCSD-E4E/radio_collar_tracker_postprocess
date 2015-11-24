#include <cstdlib>
#include <cstdint>
#include <unistd.h>
#include <getopt.h>
#include <string>
#include <fstream>

using namespace std;

int main(int argc, char** argv){
	string output_dir = "./";
	int num_samples = 4000;
	int opt;

	while ((opt = getopt(argc, argv, "o:l:")) != -1){
		switch(opt){
			case 'o':
				output_dir = optarg;
				break;
			case 'l':
				num_samples = atoi(optarg);
				break;
		}
	}
	ofstream out_stream (output_dir + "constant.raw", ios::out | ios::binary);
	uint8_t sample[2] = {255, 128};
	for(int i = 0; i < num_samples; i++){
		out_stream.write(reinterpret_cast <char*> (sample), sizeof(uint8_t) * 2);
	}
	out_stream.close();
}
