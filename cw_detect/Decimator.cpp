#include "Decimator.hpp"
#include "Sample.hpp"
#include <thread>
#include <mutex>
#include <queue>

using namespace std;

Decimator::Decimator(int sample_rate, int factor, CRFSample* (*out_queue)()): sample_rate(smaple_rate), decimation_factor(factor){


