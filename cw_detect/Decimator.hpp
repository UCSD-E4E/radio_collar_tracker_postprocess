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
class Decimator: public SampleFactory{
	private:
		/**
		 * Decimation factor
		 */
		int decimation_factor;
		/**
		 * Pointer to next sample source.
		 */
		SampleFactory* previous_module;
		/**
		 * Thread body
		 */
		void run();
		/**
		 * The thread object associated with this class
		 */
		thread* class_thread;
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
		/**
		 * Terminating sample flag
		 */
		bool has_terminating = false;
	public:
		/**
		 * Creates a Decimator class and initializes the workflow associated 
		 * with this class.  Thic constructor specifies a decimation factor.
		 * The output and input sampling rates are related with the following
		 * function: input_rate / output_rate = decimating_factor.
		 *
		 * @param sample_rate	Sampling rate of the incoming queue
		 * @param factor		Decimating factor
		 * @param previous		Object that returns in sequence the signal to
		 * 						modify.
		 */
		Decimator(int factor, SampleFactory* previous);

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
		/**
		 * Checks whether or not this module has received the terminating
		 * sample.
		 *
		 * @return true if the terminating sample has been processed, false
		 * 			otherwise.
		 */
		bool hasTerminating();
};

#endif // __DECIM_H_
