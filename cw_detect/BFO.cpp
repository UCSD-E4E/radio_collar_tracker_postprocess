#include "BFO.hpp"
#include <thread>
#include <mutex>
#include <cmath>
#include <complex>
#include "Sample.hpp"
#include <queue>
#include <iostream>

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX

using namespace std;

BFO::BFO(int frequency,
         SampleFactory* previous): OSC_freq(frequency),
	run_state(true) {
	previous_module = previous;
	// Start worker thread associated with this class
	class_thread = new thread(&BFO::run, this);
}

BFO::~BFO() {
	run_state = false;
	class_thread->join();
}

CRFSample* BFO::getNextSample() {
	if (output_queue.empty()) {
		return NULL;
	}
	output_queue_mutex.lock();
	CRFSample* retval = output_queue.front();
	output_queue.pop();
	output_queue_mutex.unlock();
	return retval;
}

void BFO::run() {
	cout << "BFO: Started" << endl;
	while (run_state) {
		// Get next sample
		CRFSample* sample = previous_module->getNextSample();
		if (!sample) {
			// TODO wait if necessary
			continue;
		}
		if(sample->isTerminating()){
			cout << "BFO: Got terminating sample" << endl;
			output_queue_mutex.lock();
			output_queue.push(sample);
			output_queue_mutex.unlock();
			break;
		}
		// Generate oscillator IQ
		double sig_time = (double)(sample->getIndex()) / sample->getSampleRate();
		complex<float> bfo_sample(sin(OSC_freq * sig_time), cos(
		                              OSC_freq * sig_time));
		// Multiply sample
		complex<float> sig_sample = sample->getData();
		sig_sample *= bfo_sample;
		sample->setData(sig_sample);
		// Queue sample
		while (output_queue.size() >= QUEUE_SIZE_MAX) {
			// TODO force wait using posix wait
		}
		output_queue_mutex.lock();
		output_queue.push(sample);
		output_queue_mutex.unlock();
	}
	cout << "BFO: Ending thread" << endl;
}

