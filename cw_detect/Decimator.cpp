#include "Decimator.hpp"
#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>
#include <iostream>
#include <cmath>

using namespace std;

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX

Decimator::Decimator(int sample_rate, int factor, SampleFactory* previous): decimation_factor(factor), run_state(true) {
	sample_freq = sample_rate;
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
	complex <float> delay_line[decimation_factor];
	float sinc[decimation_factor];

	// Generate sinc function
	float B = (float) sample_freq / decimation_factor / 4; 
	for(int i = 0; i < decimation_factor; i++){
		float t = ((float)i - decimation_factor / 2) / sample_freq;
		if(t == 0){
			sinc[i] = 2.0 * B;
			continue;
		}
		sinc[i] = 2.0 * B * sin(M_PI * 2 * B * t) / (M_PI * 2 * B * t);
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
		// Add to delay line
		delay_line[counter] = sample->getData();
		if(sample->isTerminating()){
			cout << "Decimator: Got terminating sample" << endl;
			output_queue_mutex.lock();
			output_queue.push(sample);
			output_queue_mutex.unlock();
			break;
		}
		if((counter % decimation_factor) == (decimation_factor - 1)){
			// Calculate value for sinc filter
			complex <float> average;
			for(int i = 0; i < decimation_factor; i++){
				average += delay_line[i] * sinc[i];
			}
			output_queue_mutex.lock();
			while(output_queue.size() >= QUEUE_SIZE_MAX){
				output_queue_mutex.unlock();
				// TODO force wait using posix wait
				output_queue_mutex.lock();
			}
			CRFSample* newSample = new CRFSample(index_counter, sample->getSampleRate() / decimation_factor, average);
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


