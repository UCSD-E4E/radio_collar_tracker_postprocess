#include "FileWriter.hpp"
#include <queue>
#include "Sample.hpp"
#include <string>
#include <thread>
#include <mutex>
#include <fstream>
#include <cstdint>
#include <stdexcept>
extern "C"{
	#include <sys/stat.h>
}

using namespace std;

FileWriter::FileWriter(int sample_rate, CRFSample* (*out_queue)(), int run_num)
		: sample_rate(sample_rate){
	this->run_num = run_num;
	this->next_sample = out_queue;
	this->run_state = true;
}

FileWriter::FileWriter(int sample_rate, CRFSample* (*out_queue)(), string path,
		string data_prefix, string data_suffix, string meta_prefix, 
		string meta_suffix, uint64_t block_length, int run_num){
	this->sample_rate = sample_rate;
	this->next_sample = out_queue;
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
	thread class_thread(&FileWriter::run, this);
}

FileWriter::~FileWriter(){
	run_state = false;
	class_thread.join();
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
