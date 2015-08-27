#include "FileLoader.hpp"
#include "FileWriter.hpp"
#include "Sample.hpp"
#include "LPF.hpp"
#include <iostream>

int main(int argc, char** argv){
	RFFileLoader* file_loader = new RFFileLoader(20480);
	LPF* lpf = new LPF(20480, file_loader);
	FileWriter* file_writer = new FileWriter(lpf, 1);
	file_writer->setDataDir("./");
	file_writer->start();
	file_loader->addFile("impulse.raw");
	file_loader->sendTerminating();
	while(!file_writer->hasTerminating()){
	}
	delete file_writer;
	delete lpf;
	delete file_loader;
	return 0;
}
