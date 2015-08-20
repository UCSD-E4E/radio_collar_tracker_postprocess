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
class BFO: public SampleFactory {
private:
	/**
	 * Frequency of the beat frequency oscillator.
	 */
	int OSC_freq;
	/**
	 * Pointer to the SampleFactory object that sources te samples for this
	 * module.
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
	/**
	 * Terminating symbol flag.
	 */
	bool has_terminating = false;
public:
	/**
	 * Creates a BFO class and initializes the workflow associated with
	 * this class. The BFO accepts samples at the specified sample rate,
	 * and multiplies that signal by a sinusoid of the specified frequency.
	 *
	 * @param frequency	Frequency for the beat frequency oscillator
	 * @param previous	Pointer to a SampleFactory object from which to get the
	 * 					next sample from.
	 */
	BFO(int frequency, SampleFactory* previous);
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
	/**
	 * Checks whether or not this module has received and processed the
	 * terminating sample.  If this module has received the terminating sample,
	 * the thread will clean up and exit.  If this function returns true, there
	 * is no guarantee that the thread has exited.
	 *
	 * @return	true if this module has received the terminating signal, false
	 * 			otherwise.
	 */
	bool hasTerminating();
};
#endif	// __BFO_H_
