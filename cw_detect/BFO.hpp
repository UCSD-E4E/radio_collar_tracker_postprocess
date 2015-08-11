#ifndef __BFO_H_
#define __BFO_H_
#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>

using namespace std;

/**
 * This class provides a heterodyning block.  This block multiplies the
 * incoming signal with a cosine wave of the specified frequency, thus
 * shifting the signal by the appropriate frequency.
 *
 * @author NATHAN HUI <nthui@gmail.com>
 */
class BFO {
private:
	/**
	 * Sampling rate of the incoming stream in samples per second
	 */
	int sample_rate;
	/**
	 * Frequency of the beat frequency oscillator.
	 */
	int OSC_freq;
	/**
	 * Function pointer to the function that returns the next sample
	 */
	CRFSample* (*next_sample)();
	/**
	 * Thread body
	 */
	void run();
	/**
	 * The thread object associated with this class
	 */
	thread class_thread;
	/**
	 * The output queue
	 */
	queue<CRFSample*> output_queue;
	/**
	 * Mutex for locking the output queue
	 */
	mutex output_queue_mutex;
	/**
	 * Run state variable
	 */
	bool run_state;
public:
	/**
	 * Creates a BFO class and initializes the workflow associated with
	 * this class.
	 *
	 * @param sample_rate Sampling rate of the incoming queue
	 * @param frequency	Frequency for the beat frequency oscillator
	 * @param out_queue	Function that returns in sequence the signal to
	 * 					modify.
	 */
	BFO(int sample_rate, int frequency, CRFSample * (*out_queue)());
	/**
	 * Destrpys this BFO class and deactivates the workflow associated with
	 * this class.
	 */
	~BFO();
	/**
	 * Returns the next processed signal sample in the queue.  If none exist,
	 * return null.
	 *
	 * @return the next processed sample, or NULL if none exist
	 */
	CRFSample* getNextSample();
};
#endif	// __BFO_H_
