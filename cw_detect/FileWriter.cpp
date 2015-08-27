#include "FileWriter.hpp"
#include <queue>
#include "Sample.hpp"
#include <string>
#include <thread>
#include <mutex>
#include <fstream>
#include <cstdint>
#include <stdexcept>
#include <iostream>
extern "C"{
	#include <sys/stat.h>
	#include <limits.h>
}

using namespace std;

FileWriter::FileWriter(SampleFactory* previous, int run_num){
	this->run_num = run_num;
	this->previous_module = previous;
	this->run_state = true;
}

FileWriter::FileWriter(SampleFactory* previous, string path,
		string data_prefix, string data_suffix, string meta_prefix,
		string meta_suffix, uint64_t block_length, int run_num){
	this->previous_module = previous;
	this->output_dir = path;
	this->data_prefix = data_prefix;
	this->data_suffix = data_suffix;
	this->meta_prefix = meta_prefix;
	this->meta_suffix = meta_suffix;
	this->block_length = block_length;
	this->run_num = run_num;

	// check args
	struct stat sb;
	if(stat(output_dir.c_str(), &sb)){
		// XXX ERROR
		throw invalid_argument("Could not stat directory!");
	}
	if(!S_ISDIR(sb.st_mode)){
		throw invalid_argument("Directory not a directory!");
	}
	run_state = true;
}

void FileWriter::start(){
	class_thread = new thread(&FileWriter::run, this);
}

bool FileWriter::hasTerminating(){
	return has_terminating;
}

void FileWriter::run(){
	cout << "FileWriter: Starting" << endl;
	ofstream fout;
	float sbuf[2];
	char fname_buf[PATH_MAX + NAME_MAX];
	uint64_t file_len = 0;
	int file_num = 1;
	int idle_counter = 0;

	sprintf(fname_buf, "%s/%s%06d_%06d%s", output_dir.c_str(),
			data_prefix.c_str(), run_num, file_num, data_suffix.c_str());
	fout.open(fname_buf, ios::out | ios::binary);
	if(fout.bad()){
		// TODO throw something
	}
	while(run_state){
		CRFSample* sample = previous_module->getNextSample();
		if(!sample){
			// TODO wait if necessary
			idle_counter++;
			if(idle_counter % 1000 == 0){
			}
			continue;
		}
		idle_counter = 0;
		if(sample->isTerminating()){
			cout << "FileWriter: Got terminating sample!" << endl;
			has_terminating = true;
			break;
		}
		sbuf[0] = sample->getData().real();
		sbuf[1] = sample->getData().imag();
		sample_rate = sample->getSampleRate();
		if(block_length != 0 && file_len + 2 * sizeof(float) > block_length){
			// TODO update file
			fout.close();
			sprintf(fname_buf, "%s/%s%06d_%06d%s", output_dir.c_str(),
					data_prefix.c_str(), run_num, file_num,
					data_suffix.c_str());
			fout.open(fname_buf, ios::out | ios::binary);
			file_len = 0;
			file_num++;
			cout << "FileWriter: New File: " << fname_buf << endl;
		}
		fout.write(reinterpret_cast<char*>(sbuf), 2 * sizeof(float));
		file_len += 2 * sizeof(float);
	}
	fout.close();

	// Meta file
	cout << "FileWriter: Writing Meta File" << endl;
	sprintf(fname_buf, "%s/%s%06d%s", output_dir.c_str(), meta_prefix.c_str(),
			run_num, meta_suffix.c_str());
	fout.open(fname_buf, ios::out);
	fout << "sample_rate: " << sample_rate << endl;
	fout.close();
	cout << "FileWriter: Ending thread" << endl;
}


FileWriter::~FileWriter(){
	run_state = false;
	if(class_thread){
		class_thread->join();
	}
}

void FileWriter::setMetaPrefix(string str){
	this->meta_prefix = str;
}

void FileWriter::setMetaSuffix(string str){
	this->meta_suffix = str;
}

void FileWriter::setDataPrefix(string str){
	this->data_prefix = str;
}

void FileWriter::setDataSuffix(string str){
	this->data_suffix = str;
}

void FileWriter::setDataDir(string str){
	struct stat sb;
	if(stat(str.c_str(), &sb)){
		throw invalid_argument("Could not stat directory!");
	}
	if(!S_ISDIR(sb.st_mode)){
		throw invalid_argument("Directory not a directory!");
	}
	this->output_dir = str;
}

void FileWriter::setBlockLength(uint64_t len){
	this->block_length = len;
}
