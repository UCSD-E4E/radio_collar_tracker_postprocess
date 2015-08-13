#ifndef __DECIM_H_
#define __DECIM_H_

#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>

using namespace std;

/**
 * This class provids a decimation block.  This block decimates the incoming
 * signal by a given factor, thus reducing the sampling rate of the signal.
 *
 * @author NATHAN HUI <ntlhui@gmail.com>
 */
class Decimator{
	private:
		/**
		 * Sampling rate of the incoming stream in samples per second.
		 */
		int input_sample_rate;
		/**
		 * Decimation factor
		 */
		int decimation_factor;
		/**
		 * Sampling rate of the outgoing stream in samples per second.
		 */
		int output_sample_rate;
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
		 * Output queue
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
		 * Creates a Decimator class and initializes the workflow associated 
		 * with this class.  Thic constructor specifies a decimation factor.
		 * The output and input sampling rates are related with the following
		 * function: input_rate / output_rate = decimating_factor.
		 *
		 * @param sample_rate	Sampling rate of the incoming queue
		 * @param factor		Decimating factor
		 * @param out_queue		Function that returns in sequence the signal to
		 * 						modify.
		 */
		Decimator(int sample_rate, int factor, CRFSample* (*out_queue)());

		/**
		 * Destroys this Decimator class and deactivates the workflow
		 * associated with this class.
		 */
		~Decimator();

		/**
		 * Returns the next processed signal sample in the queue.  If none
		 * exist, returns null.
		 *
		 * @return the next processed sample, or NULL if none exist.
		 */
		CRFSample* getNextSample();
};

#endif // __DECIM_H_
