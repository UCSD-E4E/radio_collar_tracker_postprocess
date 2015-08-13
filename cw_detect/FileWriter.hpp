#ifndef __FILE_WRITER_H_
#define __FILE_WRITER_H_

#include <queue>
#include "Sample.hpp"
#include <string>
#include <thread>
#include <mutex>
#include <fstream>
#include <cstdint>

/**
 * This class provides a signal processign block that writes incoming data to
 * a set of files.  The filename is specified as 
 * "[data_prefix][run_num][file_num][data_suffix]" in the specified directory.
 * A metafile is also saved with the filename 
 * "[meta_prefix][run_num][meta_suffix]" in the specified directory.  The 
 * size of each file wil not exceed the specified block length in bytes.
 */
class FileWriter{
	private:
		/**
		 * Data prefix.  Defaults to "RUN_"
		 */
		string data_prefix = "RUN_";
		/**
		 * Output directory.  Defaults to working directory/
		 */
		string output_dir = "./";
		/**
		 * Data suffix. Defaults to nothing.
		 */
		string data_suffix = "";
		/**
		 * Meta prefix.  Defaults to "META_"
		 */
		string meta_prefix = "META_";
		/**
		 * Meta suffix.  Defaults to nothing.
		 */
		string meta_suffix = "";
		/**
		 * The maximum length of a file in bytes.
		 */
		uint64_t block_length = 0;
		/**
		 * Current run number
		 */
		int run_num = 0;
		/**
		 * Thread body
		 */
		void run();
		/**
		 * Pointer to next sample runction
		 */
		CRFSample* (*next_sample)();
		/**
		 * The sampling rate of the input source
		 */
		int sample_rate;
		/**
		 * The thread associated with this class
		 */
		thread class_thread;
		/**
		 * Thread state variable
		 */
		bool run_state;
	public:
		/**
		 * Constructs a default FileWriter with the specified sampling rate, 
		 * queue callback, and run number.  Output directory defaults to 
		 * current working directory, and filenames default to
		 * "RUN_[run_num]_[file_num]" for data files, and "META_[run_num]" for
		 * meta files.
		 *
		 * @param sample_rate	Input sample rate for this block.
		 * @param out_queue		Incoming stream of data callback.
		 * @param run_num		Run number for this class
		 */
		FileWriter(int sample_rate, CRFSample* (*out_queue)(), int run_num);
		/**
		 * Constructs a default FileWriter with the specified configuration.
		 *
		 * @param sample_rate	Input sample rate for this block.
		 * @param out_queue		Input sample callback.
		 * @param path			Output path to write files to.
		 * @param data_prefix	Prefix for data files.
		 * @param data_suffix	Suffix for data files.
		 * @param meta_prefix	Prefix for meta files.
		 * @param meta_suffix	Suffix for meta files
		 * @param block_length	Maximum length for each file.
		 * @param run_num		Run number for this class.
		 */
		FileWriter(int sample_rate, CRFSample* (*out_queue)(), string path,
				string data_prefix, string data_suffix, string meta_prefix,
				string meta_suffix, uint64_t block_length, int run_num);
		/**
		 * Initializes this FileWriter object.
		 */
		void start();
		/**
		 * Destroys and deactivates this class.  Stops the thread.
		 */
		~FileWriter();
		/**
		 * Sets the meta prefix for this FileWriter object
		 *
		 * @param str	Prefix for meta files.
		 */
		void setMetaPrefix(string str);
		/**
		 * Sets the meta file suffix for this FileWriter object
		 *
		 * @param str	Suffix for meta files.
		 */
		void setMetaSuffix(string str);
		/**
		 * Sets the data file prefix for this FileWriter object
		 * @param str	Prefix for data files
		 */
		void setDataPrefix(string str);
		/**
		 * Sets the data file suffix for this FileWriter object
		 * @param str	Suffix for data files
		 */
		void setDataSuffix(string str);
		/**
		 * Sets the output directory for this FileWriter object
		 * @param str	Output directory for this object
		 */
		void setDataDir(string str);
		/**
		 * Sets the maximum file length for this FileWriter object
		 * @param len	Maximum length in bytes for this object
		 */
		void setBlockLength(uint64_t len);
};

#endif //__FILE_WRITER_H_
