#include "LPF.hpp"
#include "Sample.hpp"
#include "LPF_TAPS.hpp"
#include <thread>
#include <mutex>
#include <queue>

#ifndef QUEUE_SIZE_MAX
#define QUEUE_SIZE_MAX 1024000
#endif // QUEUE_SIZE_MAX


using namespace std;

LPF::LPF(int sample_rate, CRFSample * (*out_queue)()): sample_rate(sample_rate),
	run_state(true) {
	next_sample = out_queue;
	// Start worker thread associated with this class
	thread class_thread(&LPF::run, this);
}

LPF::~LPF() {
	run_state = false;
	class_thread.join();
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
	complex<float> ring_buf[TAP_LENGTH];
	int ring_buf_index = 0;
	while (run_state) {
		CRFSample* sample = next_sample();
		if (!sample) {
			// TODO wait if necessary
			continue;
		}
		// Store into memory buffer
		ring_buf[ring_buf_index] = sample->getData();
		// Run filter
		complex<float> sig_sample;
		complex<float> lpf_tap_c;
		for (int i = 0; i < TAP_LENGTH; i++) {
			lpf_tap_c = complex<float>(LPF_TAPS[i], 0);
			sig_sample += lpf_tap_c * ring_buf[(ring_buf_index - i) % TAP_LENGTH];
		}
		sample->setData(sig_sample);
		// Queue sample
		output_queue_mutex.lock();
		while (output_queue.size() >= QUEUE_SIZE_MAX) {
			output_queue_mutex.unlock();
			// TODO force wait using posix wait
			output_queue_mutex.lock();
		}
		output_queue.push(sample);
		output_queue_mutex.unlock();
		// Update ring buffer
		ring_buf_index++;
		ring_buf_index %= TAP_LENGTH;

	}
}
