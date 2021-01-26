#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: UHF RFID
# Author: jlejarreta@uoc.edu
# GNU Radio version: 3.7.13.5
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import rfid
import sys
import threading
import time
from gnuradio import qtgui


class uhf_rfid_get_epc(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "UHF RFID")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHF RFID")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "uhf_rfid_get_epc")
        self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))


        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 20
        self.rx_gain = rx_gain = 20
        self.print_results = print_results = 0
        self.num_taps = num_taps = [1]*25
        self.frequency = frequency = 865.7e6
        self.decim = decim = 5
        self.dac_rate = dac_rate = 1e6
        self.ampl = ampl = 0.9
        self.adc_rate = adc_rate = 100e6/50

        ##################################################
        # Blocks
        ##################################################
        self.rfid_reader = rfid.reader(int(adc_rate/decim),int(dac_rate))
        self.uhd_usrp_source = uhd.usrp_source(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
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
        self.rfid_tag_decoder = rfid.tag_decoder(int(adc_rate/decim))
        self.rfid_gate = rfid.gate(int(adc_rate/decim))

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
        self.matched_filter = filter.fir_filter_ccc(decim, (num_taps))
        self.matched_filter.declare_sample_delay(0)
        self.file_sink_source = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/source', False)
        self.file_sink_source.set_unbuffered(False)
        self.file_sink_reader = blocks.file_sink(gr.sizeof_float*1, '../misc/data/reader', False)
        self.file_sink_reader.set_unbuffered(False)
        self.file_sink_matched_filter = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/matched_filter', False)
        self.file_sink_matched_filter.set_unbuffered(False)
        self.file_sink_gate = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/gate', False)
        self.file_sink_gate.set_unbuffered(False)
        self.file_sink_decoder = blocks.file_sink(gr.sizeof_gr_complex*1, '../misc/data/decoder', False)
        self.file_sink_decoder.set_unbuffered(False)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink, 0))
        self.connect((self.matched_filter, 0), (self.file_sink_matched_filter, 0))
        self.connect((self.matched_filter, 0), (self.rfid_gate, 0))
        self.connect((self.multiply_const_ff, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rfid_gate, 0), (self.file_sink_gate, 0))
        self.connect((self.rfid_gate, 0), (self.rfid_tag_decoder, 0))
        self.connect((self.rfid_reader, 0), (self.file_sink_reader, 0))
        self.connect((self.rfid_reader, 0), (self.multiply_const_ff, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.file_sink_decoder, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.rfid_reader, 0))
        self.connect((self.uhd_usrp_source, 0), (self.file_sink_source, 0))
        self.connect((self.uhd_usrp_source, 0), (self.matched_filter, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhf_rfid_get_epc")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink.set_gain(self.tx_gain, 0)


    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source.set_gain(self.rx_gain, 0)


    def get_print_results(self):
        return self.print_results

    def set_print_results(self, print_results):
        self.print_results = print_results

    def get_num_taps(self):
        return self.num_taps

    def set_num_taps(self, num_taps):
        self.num_taps = num_taps
        self.matched_filter.set_taps((self.num_taps))

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.uhd_usrp_source.set_center_freq(self.frequency, 0)
        self.uhd_usrp_sink.set_center_freq(self.frequency, 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

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

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.uhd_usrp_source.set_samp_rate(self.adc_rate)


def main(top_block_cls=uhf_rfid_get_epc, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
