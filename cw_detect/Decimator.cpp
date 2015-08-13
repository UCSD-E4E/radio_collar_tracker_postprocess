#include "Decimator.hpp"
#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>

using namespace std;

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX

Decimator::Decimator(int sample_rate, int factor, CRFSample * (*out_queue)()): input_sample_rate(sample_rate), decimation_factor(factor), run_state(true) {
	next_sample = out_queue;
	output_sample_rate = input_sample_rate / decimation_factor;
	// Start worker thread associated with this class
	thread class_thread(&Decimator::run, this);
}

Decimator::~Decimator(){
	run_state = false;
	class_thread.join();
}

CRFSample* Decimator::getNextSample(){
	if(output_queue.empty()){
		return NULL;
	}
	output_queue_mutex.lock();
	CRFSample* retval = output_queue.front();
	output_queue.pop();
	output_queue_mutex.unlock();
	return retval;
}

void Decimator::run(){
	int counter = 0;
	int index_counter = 0;
	while(run_state){
		CRFSample* sample = next_sample();
		if(!sample){
			// TODO wait if necessary
			continue;
		}
		if((counter % decimation_factor) == 0){
			output_queue_mutex.lock();
			while(output_queue.size() >= QUEUE_SIZE_MAX){
				output_queue_mutex.unlock();
				// TODO force wait using posix wait
				output_queue_mutex.lock();
			}
			CRFSample* newSample = new CRFSample(index_counter, output_sample_rate, sample->getData());
			index_counter++;
			output_queue.push(newSample);
			output_queue_mutex.unlock();
		}
		// Discard old sample
		delete sample;
		counter++;
		counter %= decimation_factor;
	}
}


