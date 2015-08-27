#include "FileLoader.hpp"
#include "FileWriter.hpp"
#include "Sample.hpp"
#include "BFO.hpp"
#include <iostream>

int main(int argc, char** argv){
	RFFileLoader* file_loader = new RFFileLoader(2048000);
	BFO* bfo = new BFO(1, file_loader);
	FileWriter* file_writer = new FileWriter(bfo, 1);
	file_writer->setDataDir("./");
	file_writer->start();
	file_loader->addFile("constant.raw");
	file_loader->sendTerminating();
	while(!file_writer->hasTerminating()){
	}
	delete file_writer;
	delete bfo;
	delete file_loader;
	return 0;
}
