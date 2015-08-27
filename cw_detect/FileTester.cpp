#include "FileLoader.hpp"
#include "FileWriter.hpp"
#include "Sample.hpp"
#include <iostream>
#include <cstdlib>
/**
 * This program tests whether or not the FileLoader and FileWriter classes
 * work as specified.  This test loads a file, then writes it directly to disk
 * using the two specified modules.  If this test is successful, the input and
 * output files must be identical in terms of signal value stored.
 */
int main(int argc, char** argv){
	RFFileLoader* file_loader = new RFFileLoader(2048000);
	FileWriter* file_writer = new FileWriter(file_loader, 1);
	file_writer->setDataDir("./");
	file_writer->start();
	file_loader->addFile("constant.raw");
	file_loader->sendTerminating();
	while(!file_writer->hasTerminating()){
	}
	delete file_writer;
	delete file_loader;
	return 0;
}
