#include <queue>
#include "FileLoader.hpp"
#include <string>
#include "Sample.hpp"
#include <iostream>
#include <cstdint>
#include <sys/stat.h>
#include <stdexcept>
#include <iostream>
using namespace std;

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX

void RFFileLoader::run() {
	// Make variables
	cout << "FileLoader: Starting" << endl;
	string file_to_load;
	ifstream file_stream;
	uint8_t buffer[2];	// read buffer
	int index = 0;	// index of sample

	// thread body
	while (run_state) {
		// check if empty
		if (!file_queue.empty()) {
			file_queue_mutex.lock();
			// Get file
			file_to_load = file_queue.front();
			file_queue.pop();
			// Unlock
			file_queue_mutex.unlock();

			// Check for terminating signal
			if(file_to_load == "*"){
				// Got terminating signal
				cout << "FileLoader: Processed terminating signal" << endl;
				break;
			}
			cout << "FileLoader: Processing file " << file_to_load << endl;

			// Make stream
			file_stream.open(file_to_load, ios::in | ios::binary);
			// If fail
			if (file_stream.fail()) {
				cerr << "FileLoader: ERROR: Failed to open file!" << endl;
			}

			// while read 2 into the buffer
			while (file_stream.read((char*)buffer, 2)) {
				// Load into queue if space
				while (signal_queue.size() >= QUEUE_SIZE_MAX) {
					// wait
					// TODO force using posix wait
				}

				signal_queue_mutex.lock();
				CRFSample* new_sample = new CRFSample(index, sample_rate,
						buffer[0] / 128.0 - 0.5, buffer[1] / 128.0 - 0.5);
				signal_queue.push(new_sample);
				signal_queue_mutex.unlock();
				index++;
			}
			cout << "FileLoader: Loaded all samples.  Current count: " << index
				<< endl;
			// close stream
			file_stream.close();
		} else {
			// queue empty

			cout << "FileLoader: No files to process." << endl;

			// wait
			// TODO use conditional variable.  For now, just bash
		}
	}

	// Send terminating signal
	cout << "FileLoader: Sending Termination Sample" << endl;
	signal_queue_mutex.lock();
	CRFSample* new_sample = new CRFSample(index, sample_rate, 0, 0);
	new_sample->setTerminating();
	signal_queue.push(new_sample);
	signal_queue_mutex.unlock();
	cout << "FileLoader: Ending thread" << endl;
}

RFFileLoader::RFFileLoader(int sample_rate) : sample_rate(sample_rate),
	run_state(true) {
		// Start worker thread associated with this class
		this->class_thread = new thread(&RFFileLoader::run, this);
	}

void RFFileLoader::addFile(string filename) {
	// Check file is good
	struct stat buffer;
	stat(filename.c_str(), &buffer);
	if (!S_ISREG(buffer.st_mode)) {
		throw invalid_argument("Failed to open file!");
	}
	// Add to queue
	file_queue_mutex.lock();
	file_queue.push(filename);
	file_queue_mutex.unlock();
	// clean up
}

RFFileLoader::~RFFileLoader() {
	this->class_thread->join();
}

void RFFileLoader::sendTerminating(){
	file_queue_mutex.lock();
	file_queue.push("*");
	file_queue_mutex.unlock();
}

CRFSample* RFFileLoader::getNextSample() {
	if (signal_queue.empty()) {
		return NULL;
	}
	signal_queue_mutex.lock();
	CRFSample* retval = signal_queue.front();
	signal_queue.pop();
	signal_queue_mutex.unlock();
	return retval;
}
