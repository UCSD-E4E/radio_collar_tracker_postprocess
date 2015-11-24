/**
 * This program is designed to integrate the modules in the Radio Collar
 * Tracker post-processing code.
 *
 * @author NATHAN HUI <ntlhui@gmail.com>
 */
#include "FileLoader.hpp"
#include "FileWriter.hpp"
#include "Sample.hpp"
#include "Decimator.hpp"
#include "BFO.hpp"
#include "LPF.hpp"
#include <iostream>
#include <unistd.h>
#include <getopt.h>
#include <cstdlib>

/**
 * This is the main routine for this program.  This function initializes and
 * sets up the various module associated with this program.
 *
 * @param argc	Number of command line arguments
 * @param argv	Array of C strings representing arguments
 */
int main(int argc, char** argv){
	int opt;
	string input_dir = "./";
	string  output_dir = "./";
	int runNum = -1;
	int bfo_freq = 2000;

	while ((opt=getopt(argc, argv, "hi:o:r:f:")) != -1){
		switch (opt){
			case 'h':
			case '?':
				// TODO: printUsage()
				exit(0);
			case 'i':
				input_dir = optarg;
				break;
			case 'o':
				output_dir = optarg;
				break;
			case 'r':
				runNum = atoi(optarg);
				break;
			case 'f':
				bfo_freq = atoi(optarg);
		}
	}
	cout << "Input Directory: " << input_dir << endl;
	cout << "Output Directory: " << output_dir << endl;
	cout << "Run Number: " << runNum << endl;
	cout << "Frequency: " << bfo_freq << endl;

	if(runNum < 0){
		cerr << "Starter: ERROR bad runNum" << endl;
		exit(-1);
	}

	cout << "Starter: Loading classes" << endl;
	RFFileLoader* file_loader = new RFFileLoader(2048000);
	BFO* bfo = new BFO(bfo_freq, file_loader);
	Decimator* pre_decimator = new Decimator(100, bfo);
	LPF* lpf = new LPF(20480, pre_decimator);
	FileWriter* file_writer = new FileWriter(lpf, runNum);
	file_writer->setDataDir(output_dir);
	file_writer->start();
	cout << "Starter: Adding file" << endl;
	for(int i = optind; i < argc; i++){
		file_loader->addFile(input_dir + string(argv[i]));
	}
	cout << "Starter: Signaling Termination" << endl;
	file_loader->sendTerminating();
	cout << "Starter: Waiting for pipeline to finish" << endl;
	while(!file_writer->hasTerminating()){
	}
	cout << "Starter: Deleting classes" << endl;
	delete file_writer;
	delete pre_decimator;
	delete lpf;
	delete bfo;
	delete file_loader;
	cout << "Starter: Ending thread" << endl;
	return 0;
}
