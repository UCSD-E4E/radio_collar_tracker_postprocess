#include "LPF.hpp"
#include "Sample.hpp"
#include "20480_LPF_TAPS.hpp"
#include <thread>
#include <mutex>
#include <queue>
#include <iostream>
#include <stdexcept>

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX


using namespace std;

LPF::LPF(int sample_rate, SampleFactory* previous): sample_rate(sample_rate),
	run_state(true) {
	previous_module = previous;
	if(sample_rate != SAMPLING_RATE){
		throw invalid_argument("Sampling rates do not match!");
	}
	// Start worker thread associated with this class
	class_thread = new thread(&LPF::run, this);
}

LPF::~LPF() {
	run_state = false;
	class_thread->join();
}

CRFSample* LPF::getNextSample() {
	if (output_queue.empty()) {
		return NULL;
	}
	output_queue_mutex.lock();
	CRFSample* retval = output_queue.front();
	output_queue.pop();
	output_queue_mutex.unlock();
	return retval;
}

void LPF::run() {
	cout << "LPF: Starting" << endl;
	complex<float> ring_buf[TAP_LENGTH];
	int ring_buf_index = 0;
	int idle_counter = 0;
	while (run_state) {
		CRFSample* sample = previous_module->getNextSample();
		if (!sample) {
			// TODO wait if necessary
			idle_counter++;
			if(idle_counter % 1000 == 0){
			}
			continue;
		}
		idle_counter = 0;
		if(sample->isTerminating()){
			cout << "LPF: got terminating sample" << endl;
			output_queue_mutex.lock();
			output_queue.push(sample);
			output_queue_mutex.unlock();
			has_terminating = true;
			break;
		}
		if(sample->getSampleRate() != SAMPLING_RATE){
			throw domain_error("Sampling Rates don't match!");
		}
		// Store into memory buffer
		ring_buf[ring_buf_index] = sample->getData();
		// Run filter
		complex<float> sig_sample;
		complex<float> lpf_tap_c;
		for (int i = 0; i < ring_buf_index + 1; i++) {
			lpf_tap_c = complex<float>(LPF_TAPS[i], 0);
			sig_sample += lpf_tap_c * ring_buf[ring_buf_index - i];
		}
		for(int i = ring_buf_index + 1; i < TAP_LENGTH; i++){
			lpf_tap_c = complex<float>(LPF_TAPS[i], 0);
			sig_sample += lpf_tap_c * ring_buf[TAP_LENGTH + ring_buf_index - i];
		}
		sample->setData(sig_sample);
		// Queue sample
		while (output_queue.size() >= QUEUE_SIZE_MAX) {
			// TODO force wait using posix wait
		}
		output_queue_mutex.lock();
		output_queue.push(sample);
		output_queue_mutex.unlock();
		// Update ring buffer
		ring_buf_index++;
		ring_buf_index %= TAP_LENGTH;

	}
	cout << "LPF: Ending thread" << endl;
}

bool LPF::hasTerminating(){
	return has_terminating;
}
