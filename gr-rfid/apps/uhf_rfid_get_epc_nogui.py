#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: UHF RFID
# Author: jlejarreta@uoc.edu
# GNU Radio version: 3.7.13.5
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import rfid
import threading
import time


class uhf_rfid_get_epc_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "UHF RFID")

        ##################################################
        # Variables
        ##################################################
        self.adc_rate = adc_rate = 2e6
        self.tx_gain = tx_gain = 10
        self.taps_fir_averaging_samples = taps_fir_averaging_samples = [1]*25
        self.samplerate_rfidblocks = samplerate_rfidblocks = adc_rate/1
        self.rx_gain = rx_gain = 20
        self.print_results = print_results = 0
        self.frequency = frequency = 865.7e6
        self.dac_rate = dac_rate = 1*1e6
        self.ampl = ampl = 0.8

        ##################################################
        # Blocks
        ##################################################
        self.rfid_reader = rfid.reader(int(samplerate_rfidblocks),int(dac_rate))
        self.uhd_usrp_source = uhd.usrp_source(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		otw_format='sc16',
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source.set_samp_rate(adc_rate)
        self.uhd_usrp_source.set_center_freq(frequency, 0)
        self.uhd_usrp_source.set_gain(rx_gain, 0)
        self.uhd_usrp_source.set_antenna('RX2', 0)
        self.uhd_usrp_source.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source.set_auto_iq_balance(False, 0)
        self.uhd_usrp_sink = uhd.usrp_sink(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink.set_samp_rate(dac_rate)
        self.uhd_usrp_sink.set_center_freq(frequency, 0)
        self.uhd_usrp_sink.set_gain(tx_gain, 0)
        self.uhd_usrp_sink.set_antenna('TX/RX', 0)
        self.rfid_tag_decoder = rfid.tag_decoder(int(samplerate_rfidblocks))
        self.rfid_gate = rfid.gate(int(samplerate_rfidblocks))

        def _print_results_probe():
            while True:
                val = self.rfid_reader.print_results()
                try:
                    self.set_print_results(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _print_results_thread = threading.Thread(target=_print_results_probe)
        _print_results_thread.daemon = True
        _print_results_thread.start()

        self.multiply_const_ff = blocks.multiply_const_ff(ampl)
        self.fir_filter = filter.fir_filter_ccc(1, (taps_fir_averaging_samples))
        self.fir_filter.declare_sample_delay(0)
        self.file_sink_source = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/source', False)
        self.file_sink_source.set_unbuffered(False)
        self.file_sink_reader_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/file_sink', False)
        self.file_sink_reader_0.set_unbuffered(False)
        self.file_sink_reader = blocks.file_sink(gr.sizeof_float*1, '../misc/data/reader', False)
        self.file_sink_reader.set_unbuffered(False)
        self.file_sink_matched_filter = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/matched_filter', False)
        self.file_sink_matched_filter.set_unbuffered(False)
        self.file_sink_gate = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/gate', False)
        self.file_sink_gate.set_unbuffered(False)
        self.file_sink_decoder2 = blocks.file_sink(gr.sizeof_float*1, '../misc/data/decoder_float', False)
        self.file_sink_decoder2.set_unbuffered(False)
        self.file_sink_decoder = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/decoder_complex', False)
        self.file_sink_decoder.set_unbuffered(False)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.file_sink_reader_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink, 0))
        self.connect((self.fir_filter, 0), (self.file_sink_matched_filter, 0))
        self.connect((self.fir_filter, 0), (self.rfid_gate, 0))
        self.connect((self.multiply_const_ff, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rfid_gate, 0), (self.file_sink_gate, 0))
        self.connect((self.rfid_gate, 0), (self.rfid_tag_decoder, 0))
        self.connect((self.rfid_reader, 0), (self.file_sink_reader, 0))
        self.connect((self.rfid_reader, 0), (self.multiply_const_ff, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.file_sink_decoder, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.file_sink_decoder2, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.rfid_reader, 0))
        self.connect((self.uhd_usrp_source, 0), (self.file_sink_source, 0))
        self.connect((self.uhd_usrp_source, 0), (self.fir_filter, 0))

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.set_samplerate_rfidblocks(self.adc_rate/1)
        self.uhd_usrp_source.set_samp_rate(self.adc_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink.set_gain(self.tx_gain, 0)


    def get_taps_fir_averaging_samples(self):
        return self.taps_fir_averaging_samples

    def set_taps_fir_averaging_samples(self, taps_fir_averaging_samples):
        self.taps_fir_averaging_samples = taps_fir_averaging_samples
        self.fir_filter.set_taps((self.taps_fir_averaging_samples))

    def get_samplerate_rfidblocks(self):
        return self.samplerate_rfidblocks

    def set_samplerate_rfidblocks(self, samplerate_rfidblocks):
        self.samplerate_rfidblocks = samplerate_rfidblocks

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source.set_gain(self.rx_gain, 0)


    def get_print_results(self):
        return self.print_results

    def set_print_results(self, print_results):
        self.print_results = print_results

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.uhd_usrp_source.set_center_freq(self.frequency, 0)
        self.uhd_usrp_sink.set_center_freq(self.frequency, 0)

    def get_dac_rate(self):
        return self.dac_rate

    def set_dac_rate(self, dac_rate):
        self.dac_rate = dac_rate
        self.uhd_usrp_sink.set_samp_rate(self.dac_rate)

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.multiply_const_ff.set_k(self.ampl)


def main(top_block_cls=uhf_rfid_get_epc_nogui, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
