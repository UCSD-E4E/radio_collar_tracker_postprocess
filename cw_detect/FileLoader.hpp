#ifndef __FILE_LOADER_H_
#define __FILE_LOADER_H_

#include <queue>
#include "Sample.hpp"
#include <string>
#include <thread>
#include <mutex>
#include <fstream>
using namespace std;

/**
 * This class creates a thread that loads a set of files into a queue for
 * processing.  This class reads only complex IQ files formatted as 8 bit
 * integer I followed by 8 bit integer Q components.  This class expects the
 * components to be formatted as little-endian unsigned 8 bit integers.  The
 * integers will be interpreted as being centered around 128, that is, 0 to 255
 * maps proportionally to the range -1.0 to 1.0.
 *
 * @author NATHAN HUI
 */
class RFFileLoader {
private:
	/**
	 * Internal file queue
	 */
	queue<string> file_queue;
	/**
	 * Signal sample queue
	 */
	queue<CRFSample> signal_queue;
	/**
	 * Thread function
	 */
	void run();
	/**
	 * The thread object associated by this class
	 */
	thread class_thread;
	/**
	 * Mutex for locking the file queue
	 */
	mutex file_queue_mutex;
	/**
	 * Mutex for locking the signal queue
	 */
	mutex signal_queue_mutex;
	/**
	 * Sampling rate for this sequence of files
	 */
	int sample_rate;
	/**
	 * Run variable
	 */
	bool run_state;
public:
	/**
	 * Creates a FileLoader class
	 */
	RFFileLoader(int sample_rate);
	/**
	 * Destroys the FileLoader class
	 */
	~RFFileLoader();
	/**
	 * Specifies a file to add to the queue by filename.  This adds the filename
	 * to an internal queue, which the worker thread will pick up and add to the
	 * signal processing queue.  Thus, the file will be added in order received
	 * by this class.
	 *
	 * @param filename Path to file to add to queue
	 */
	void addFile(string filename);
	/**
	 * Returns the next signal sample in the queue.
	 */
	CRFSample getNextSample();
};

#endif //__FILE_LOADER_H_
