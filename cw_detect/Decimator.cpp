#include "Decimator.hpp"
#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>
#include <iostream>

using namespace std;

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX

Decimator::Decimator(int factor, SampleFactory* previous): decimation_factor(factor), run_state(true) {
	previous_module = previous;
	// Start worker thread associated with this class
	class_thread = new thread(&Decimator::run, this);
}

Decimator::~Decimator(){
	run_state = false;
	class_thread->join();
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

bool Decimator::hasTerminating(){
	return has_terminating;
}

void Decimator::run(){
	cout << "Decimator: Starting" << endl;
	int counter = 0;
	int index_counter = 0;
	int idle_counter = 0;
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
			cout << "Decimator: Got terminating sample" << endl;
			output_queue_mutex.lock();
			output_queue.push(sample);
			output_queue_mutex.unlock();
			break;
		}
		if((counter % decimation_factor) == 0){
			output_queue_mutex.lock();
			while(output_queue.size() >= QUEUE_SIZE_MAX){
				output_queue_mutex.unlock();
				// TODO force wait using posix wait
				output_queue_mutex.lock();
			}
			CRFSample* newSample = new CRFSample(index_counter, sample->getSampleRate() / decimation_factor, sample->getData());
			index_counter++;
			output_queue.push(newSample);
			output_queue_mutex.unlock();
		}
		// Discard old sample
		delete sample;
		counter++;
		counter %= decimation_factor;
	}
	cout << "Decimator: Ending thread" << endl;
}


