#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Sep 10 07:11:22 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class top_block(gr.top_block):

    def __init__(self, bfo_freq=-11583, input_file="/dev/null", output_file="/dev/null"):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.bfo_freq = bfo_freq
        self.input_file = input_file
        self.output_file = output_file

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2048000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=100,
                taps=None,
                fractional_bw=None,
        )
        self.fir_filter_xxx_0 = filter.fir_filter_ccf(1, ([0.0008687428780831397, 0.0013175825588405132, -0.001188602764159441, -0.002553905127570033, 0.002098661847412586, 0.0053000920452177525, -0.003509196685627103, -0.010158673860132694, 0.005261188838630915, 0.01802591234445572, -0.007146207615733147, -0.030604897066950798, 0.008933454751968384, 0.052204325795173645, -0.010400292463600636, -0.09877216070890427, 0.011362021788954735, 0.3152790367603302, 0.48736584186553955, 0.3152790367603302, 0.011362021788954735, -0.09877216070890427, -0.010400292463600636, 0.052204325795173645, 0.008933454751968384, -0.030604897066950798, -0.007146207615733147, 0.01802591234445572, 0.005261188838630915, -0.010158673860132694, -0.003509196685627103, 0.0053000920452177525, 0.002098661847412586, -0.002553905127570033, -0.001188602764159441, 0.0013175825588405132, 0.0008687428780831397]))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1/128.0, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, input_file, False)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, output_file, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_float*1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, bfo_freq, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_deinterleave_0, 0))    
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_uchar_to_float_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.fir_filter_xxx_0, 0))    


    def get_bfo_freq(self):
        return self.bfo_freq

    def set_bfo_freq(self, bfo_freq):
        self.bfo_freq = bfo_freq
        self.analog_sig_source_x_0.set_frequency(self.bfo_freq)

    def get_input_file(self):
        return self.input_file

    def set_input_file(self, input_file):
        self.input_file = input_file
        self.blocks_file_source_0.open(self.input_file, False)

    def get_output_file(self):
        return self.output_file

    def set_output_file(self, output_file):
        self.output_file = output_file
        self.blocks_file_sink_1.open(self.output_file)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-f", "--bfo-freq", dest="bfo_freq", type="intx", default=-11583,
        help="Set freq [default=%default]")
    parser.add_option("-i", "--input-file", dest="input_file", type="string", default="/dev/null",
        help="Set input [default=%default]")
    parser.add_option("-o", "--output-file", dest="output_file", type="string", default="/dev/null",
        help="Set output [default=%default]")
    (options, args) = parser.parse_args()
    tb = top_block(bfo_freq=options.bfo_freq, input_file=options.input_file, output_file=options.output_file)
    tb.start()
    tb.wait()
