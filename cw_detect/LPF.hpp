#ifndef __LPF_H_
#define __LPF_H_

#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>

using namespace std;

/**
 * This class represents a FIR Low Pass Filter block.  This filter implements a
 * 5 kHz passband with a 1 kHz transition band, with a 40 dB attenuation in the
 * stopband.  Filter coefficients were generated using the GNU Radio Companion
 * Filter Design tool.
 *
 * @author NATHAN HUI <ntlhui@gmail.com>
 */
class LPF: public SampleFactory {
private:
	/**
	 * Internal sampling rate
	 */
	int sample_rate;
	/**
	 * Pointer to the SampleFactory object that supplies the next sample.
	 */
	SampleFactory* previous_module;
	/**
	 * Thread body
	 */
	void run();
	/**
	 * Thread associated with this class
	 */
	thread* class_thread;
	/**
	 * Output signal queue
	 */
	queue<CRFSample*> output_queue;
	/**
	 * Output queue mutex
	 */
	mutex output_queue_mutex;
	/**
	 * Thread state variable
	 */
	bool run_state;
	/**
	 * Terminating sample flag
	 */
	bool has_terminating = false;
public:
	/**
	 * Creates and initializes a new LPF object.
	 *
	 * @param sample_rate Sampling rate of the incoming queue
	 * @param previous	Pointer to a SampleFactory from which to source the
	 * 					next samples to process.
	 */
	LPF(int sample_rate, SampleFactory* previous);
	/**
	 * Deactivates and destroys this LPF object.
	 */
	~LPF();
	/**
	 * Returns the next processed signal sample in the queue.  If none exist,
	 * return null.
	 *
	 * @return the next processed sample, or NULL if none exist
	 */
	CRFSample* getNextSample();
	/**
	 * Checks whether or not this module has received and processed the
	 * terminating sample.
	 *
	 * @return	true if this module has received the terminating sample, false
	 * 			otherwise.
	 */
	bool hasTerminating();
};

#endif // __LPF_H_
