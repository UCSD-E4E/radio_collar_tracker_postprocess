#ifndef __SAMPLE_H_
#define __SAMPLE_H_

#include <complex>

using namespace std;
/**
 * This class represents a sample of data in a stream of data.
 */
class Sample {
private:
	/**
	 * Defines the sampling rate of this sample in samples per second
	 */
	int sample_rate;
	/**
	 * Defines the index of this sample, zero based
	 */
	int index;
public:
	/**
	 * Creates a Sample object with a specified index and sampling rate
	 */
	Sample(int index, int sample_rate);
};

/**
 * This class represetns a single complex RF data sample.
 */
class CRFSample: public Sample {
private:
	complex<float> sample;
public:
	/**
	 * Creates a new RFSample, with it's own copy of the complex sample.
	 *
	 * @param index	The index of this sample in the stream, starting at 0
	 * @param sample_rate	The sampling rate of this stream.
	 * @param sample	The sample value this object should reflect
	 */
	CRFSample(int index, int sample_rate, complex<float> sample);

	/**
	 * Creates a new RFSample, with the complex sample set to i + j * q, where j
	 * is the imaginary unit.
	 *
	 * @param index	The index of this sample in the stream, starting at 0
	 * @param sample_rate	The sampling rate of this stream.
	 * @param i	The in-phase or real part of the complex value
	 * @param q	The quadrature or imaginary part of the complex value
	 */
	CRFSample(int index, int sample_rate, float i, float q);

	/**
	 * Returns a copy of the complex data stored internally.
	 *
	 * @return	The complex value represented by this sample
	 */
	complex<float> get_data();

	/**
	 * Sets the internal data to reflect the value of the new data provided.
	 * Specifically, this sample will represent the same time, but with sample
	 * value set to be equal to new_data.
	 *
	 * @param new_data	The new data this object should reflect.
	 */
	void set_data(complex<float> new_data);

	/**
	 * Sets the interal data to reflect the value of the new data provided.
	 * Specifically, this sample will represent the same time, but with sample
	 * value i + j * q, where j is the imaginary unit.
	 *
	 * @param i The in-phase or real part of the complex value.
	 * @param q The quadrature or imaginary part of the complex value.
	 */
	void set_data(float i, float q);
};

#endif // __SAMPLE_H_
