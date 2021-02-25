#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: UHF RFID GnuRadio decoder
# Author: jlejarreta@uoc.edu
# Description: UHF RFID GnuRadio decoder
# GNU Radio version: 3.7.13.5
##################################################
import threading

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

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import rfid
import sip
import sys
import threading
import time
from gnuradio import qtgui


class uhf_rfid_blocks_analysis(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "UHF RFID GnuRadio decoder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHF RFID GnuRadio decoder")
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

        self.settings = Qt.QSettings("GNU Radio", "uhf_rfid_blocks_analysis")
        self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))


        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.adc_rate = adc_rate = 2e6
        self.tx_gain_antenna = tx_gain_antenna = 7.3
        self.tx_gain = tx_gain = 12
        self.taps_fir_averaging_samples = taps_fir_averaging_samples = [1]*25
        self.samplerate_rfidblocks = samplerate_rfidblocks = adc_rate/1
        self.rx_gain_antenna = rx_gain_antenna = 7.3
        self.rx_gain = rx_gain = 18
        self.print_results = print_results = 0
        self.frequency = frequency = 865.7e6
        self.dac_rate = dac_rate = 2*1e6
        self.ampl = ampl = 0.8
        self.GUI_samples = GUI_samples = int(0.7*(44+62+16+62+18+62+96+62)*(adc_rate*24/1000000))

        ##################################################
        # Blocks
        ##################################################
        self.rfid_reader = rfid.reader(int(samplerate_rfidblocks),int(dac_rate))
        self.gui_tab = Qt.QTabWidget()
        self.gui_tab_widget_0 = Qt.QWidget()
        self.gui_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_0)
        self.gui_tab_grid_layout_0 = Qt.QGridLayout()
        self.gui_tab_layout_0.addLayout(self.gui_tab_grid_layout_0)
        self.gui_tab.addTab(self.gui_tab_widget_0, 'Source')
        self.gui_tab_widget_1 = Qt.QWidget()
        self.gui_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_1)
        self.gui_tab_grid_layout_1 = Qt.QGridLayout()
        self.gui_tab_layout_1.addLayout(self.gui_tab_grid_layout_1)
        self.gui_tab.addTab(self.gui_tab_widget_1, 'FIR Filter')
        self.gui_tab_widget_2 = Qt.QWidget()
        self.gui_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_2)
        self.gui_tab_grid_layout_2 = Qt.QGridLayout()
        self.gui_tab_layout_2.addLayout(self.gui_tab_grid_layout_2)
        self.gui_tab.addTab(self.gui_tab_widget_2, 'Gate')
        self.gui_tab_widget_3 = Qt.QWidget()
        self.gui_tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_3)
        self.gui_tab_grid_layout_3 = Qt.QGridLayout()
        self.gui_tab_layout_3.addLayout(self.gui_tab_grid_layout_3)
        self.gui_tab.addTab(self.gui_tab_widget_3, 'Tag_Decoder')
        self.gui_tab_widget_4 = Qt.QWidget()
        self.gui_tab_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.gui_tab_widget_4)
        self.gui_tab_grid_layout_4 = Qt.QGridLayout()
        self.gui_tab_layout_4.addLayout(self.gui_tab_grid_layout_4)
        self.gui_tab.addTab(self.gui_tab_widget_4, 'Reader')
        self.top_grid_layout.addWidget(self.gui_tab)
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
        self.qtgui_time_sink_x_0_2_1 = qtgui.time_sink_f(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Float Output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_2_1.set_update_time(1)
        self.qtgui_time_sink_x_0_2_1.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_2_1.set_y_label('bit', '?')

        self.qtgui_time_sink_x_0_2_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_2_1.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 0.2, 0, 0, "rfid_status")
        self.qtgui_time_sink_x_0_2_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_2_1.enable_grid(True)
        self.qtgui_time_sink_x_0_2_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2_1.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_2_1.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_2_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2_1.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_4.addWidget(self._qtgui_time_sink_x_0_2_1_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.gui_tab_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_2_0_0 = qtgui.time_sink_c(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Complex output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_2_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_2_0_0.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_2_0_0.set_y_label('Bit', '?')

        self.qtgui_time_sink_x_0_2_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 0.2, 0, 0, "rfid_status")
        self.qtgui_time_sink_x_0_2_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_2_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2_0_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_2_0_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_2_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_2_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_4.addWidget(self._qtgui_time_sink_x_0_2_0_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.gui_tab_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_2_0 = qtgui.time_sink_c(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Complex output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_2_0.set_update_time(1)
        self.qtgui_time_sink_x_0_2_0.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_2_0.set_y_label('Bit', '?')

        self.qtgui_time_sink_x_0_2_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_2_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "rfid_status")
        self.qtgui_time_sink_x_0_2_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_2_0.enable_grid(True)
        self.qtgui_time_sink_x_0_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_2_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_2_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_2_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_2_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.gui_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_2 = qtgui.time_sink_f(
        	18, #size
        	adc_rate, #samp_rate
        	'Float Output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_2.set_update_time(1)
        self.qtgui_time_sink_x_0_2.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_2.set_y_label('bit', '?')

        self.qtgui_time_sink_x_0_2.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_2.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "rfid_status")
        self.qtgui_time_sink_x_0_2.enable_autoscale(True)
        self.qtgui_time_sink_x_0_2.enable_grid(True)
        self.qtgui_time_sink_x_0_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_2.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_2_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.gui_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0 = qtgui.time_sink_c(
        	GUI_samples, #size
        	int(samplerate_rfidblocks), #samp_rate
        	'Amplitude/Magnitude', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_1_0.set_update_time(1)
        self.qtgui_time_sink_x_0_1_0.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_1_0.set_y_label('Amplitude', '?')

        self.qtgui_time_sink_x_0_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_NEG, 0, 0, 2, "rfid_status")
        self.qtgui_time_sink_x_0_1_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_1_0.enable_grid(True)
        self.qtgui_time_sink_x_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_1_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 0, 0, 0, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 0, 0, 0, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 0.0, 0.0, 0.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(4):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_1_0_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.gui_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Amplitude/Magnitude', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_1.set_update_time(1)
        self.qtgui_time_sink_x_0_1.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', '?')

        self.qtgui_time_sink_x_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 2, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_1.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_1_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.gui_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_c(
        	GUI_samples, #size
        	int(samplerate_rfidblocks), #samp_rate
        	'Phase Plot', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-180, 180)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Phase', 'deg')

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_NEG, 2, 0, 2, "rfid_status")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_0_0_0.disable_legend()

        labels = ['Phase', 'Magnitude', '', '', '',
                  '', '', '', '', '']
        widths = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 0.0, 0.0, 0.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(4):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.gui_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Phase Plot', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-180, 180)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Phase', 'deg')

        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 2, 0, 1, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_0_0.disable_legend()

        labels = ['Phase', 'Magnitude', '', '', '',
                  '', '', '', '', '']
        widths = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 0.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.gui_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Phase Plot', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0.set_y_axis(-180, 180)

        self.qtgui_time_sink_x_0_0.set_y_label('Phase', 'deg')

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 0.2, 0, 1, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['Phase', 'Magnitude', '', '', '',
                  '', '', '', '', '']
        widths = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 0, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 0.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	GUI_samples, #size
        	adc_rate, #samp_rate
        	'Amplitude/Magnitude', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(1)
        self.qtgui_time_sink_x_0.set_y_axis(0, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', '?')

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_NEG, 0.2, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_2_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	20,
                -0.1,
                1.1,
        	'Float output',
        	1
        )

        self.qtgui_histogram_sink_x_0_2_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0_2_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_2_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_2_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0_2_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_2_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_2_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_2_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_2_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_2_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_2_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_2_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_2_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_4.addWidget(self._qtgui_histogram_sink_x_0_2_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.gui_tab_grid_layout_4.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_2 = qtgui.histogram_sink_f(
        	16,
        	20,
                -0.1,
                1.1,
        	'Float output',
        	1
        )

        self.qtgui_histogram_sink_x_0_2.set_update_time(1)
        self.qtgui_histogram_sink_x_0_2.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_2.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_2.enable_grid(False)
        self.qtgui_histogram_sink_x_0_2.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_2.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_2.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_2.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_2_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_2.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_3.addWidget(self._qtgui_histogram_sink_x_0_2_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.gui_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_1_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	200,
                -0.1,
                1.1,
        	'Normalized magnitude RX',
        	1
        )

        self.qtgui_histogram_sink_x_0_1_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0_1_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_1_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_1_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0_1_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_1_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_1_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_2.addWidget(self._qtgui_histogram_sink_x_0_1_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.gui_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_1 = qtgui.histogram_sink_f(
        	GUI_samples,
        	200,
                -0.1,
                1.1,
        	'Normalized magnitude RX',
        	1
        )

        self.qtgui_histogram_sink_x_0_1.set_update_time(1)
        self.qtgui_histogram_sink_x_0_1.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_1.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_1.enable_grid(False)
        self.qtgui_histogram_sink_x_0_1.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_1.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_1_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_1.addWidget(self._qtgui_histogram_sink_x_0_1_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.gui_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_0_0_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	360,
                -180,
                180,
        	'Phase (deg) Histogram',
        	1
        )

        self.qtgui_histogram_sink_x_0_0_0_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0_0_0_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_0_0_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0_0_0_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_0_0_0.disable_legend()

        labels = ['Phase', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_2.addWidget(self._qtgui_histogram_sink_x_0_0_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.gui_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_0_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	360,
                -180,
                180,
        	'Phase (deg) Histogram',
        	1
        )

        self.qtgui_histogram_sink_x_0_0_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_0_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_0_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0_0_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_0_0.disable_legend()

        labels = ['Phase', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_1.addWidget(self._qtgui_histogram_sink_x_0_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.gui_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	360,
                -180,
                180,
        	'Phase (deg) Histogram',
        	1
        )

        self.qtgui_histogram_sink_x_0_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0_0.disable_legend()

        labels = ['Phase', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
        	GUI_samples,
        	200,
                -0.1,
                1.1,
        	'Normalized magnitude RX',
        	1
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)

        if not False:
          self.qtgui_histogram_sink_x_0.disable_legend()

        labels = ['Magnitude', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.gui_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
        	GUI_samples, #size
        	'Complex output', #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(1.0)
        self.qtgui_const_sink_x_0_0.set_y_axis(-0.1, 1.0)
        self.qtgui_const_sink_x_0_0.set_x_axis(-0.1, 1)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 10.0, 0, "rfid_status")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_4.addWidget(self._qtgui_const_sink_x_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.gui_tab_grid_layout_4.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	GUI_samples, #size
        	'Complex output', #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(1.0)
        self.qtgui_const_sink_x_0.set_y_axis(-1.0, 1.0)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 21)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 10.0, 0, "rfid_status")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.gui_tab_grid_layout_3.addWidget(self._qtgui_const_sink_x_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.gui_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(2, 3):
            self.gui_tab_grid_layout_3.setColumnStretch(c, 1)

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
        self.blocks_tag_share_0 = blocks.tag_share(gr.sizeof_gr_complex, gr.sizeof_float, 1)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'Ettus RX Source Tags', ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vff((57.295779513082320876798154814105, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((57.295779513082320876798154814105, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((57.295779513082320876798154814105, ))
        self.blocks_float_to_complex_0_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_magphase_0_0_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0_0 = blocks.complex_to_magphase(1)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_complex_to_magphase_0_0, 1), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.qtgui_histogram_sink_x_0_1, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 1))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_complex_to_magphase_0_0_0, 0), (self.blocks_float_to_complex_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0_0, 1), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0_0, 0), (self.qtgui_histogram_sink_x_0_1_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_tag_share_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0_0, 0), (self.qtgui_time_sink_x_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_histogram_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_histogram_sink_x_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.qtgui_histogram_sink_x_0_0_0_0, 0))
        self.connect((self.blocks_tag_share_0, 0), (self.file_sink_reader_0, 0))
        self.connect((self.blocks_tag_share_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_tag_share_0, 0), (self.qtgui_time_sink_x_0_2_0_0, 0))
        self.connect((self.blocks_tag_share_0, 0), (self.uhd_usrp_sink, 0))
        self.connect((self.fir_filter, 0), (self.blocks_complex_to_magphase_0_0, 0))
        self.connect((self.fir_filter, 0), (self.file_sink_matched_filter, 0))
        self.connect((self.fir_filter, 0), (self.rfid_gate, 0))
        self.connect((self.multiply_const_ff, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.rfid_gate, 0), (self.blocks_complex_to_magphase_0_0_0, 0))
        self.connect((self.rfid_gate, 0), (self.file_sink_gate, 0))
        self.connect((self.rfid_gate, 0), (self.qtgui_time_sink_x_0_0_0_0, 1))
        self.connect((self.rfid_gate, 0), (self.qtgui_time_sink_x_0_1_0, 1))
        self.connect((self.rfid_gate, 0), (self.rfid_tag_decoder, 0))
        self.connect((self.rfid_reader, 0), (self.blocks_tag_share_0, 1))
        self.connect((self.rfid_reader, 0), (self.file_sink_reader, 0))
        self.connect((self.rfid_reader, 0), (self.multiply_const_ff, 0))
        self.connect((self.rfid_reader, 0), (self.qtgui_histogram_sink_x_0_2_0, 0))
        self.connect((self.rfid_reader, 0), (self.qtgui_time_sink_x_0_2_1, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.file_sink_decoder, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.file_sink_decoder2, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.qtgui_histogram_sink_x_0_2, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.qtgui_time_sink_x_0_2, 0))
        self.connect((self.rfid_tag_decoder, 1), (self.qtgui_time_sink_x_0_2_0, 0))
        self.connect((self.rfid_tag_decoder, 0), (self.rfid_reader, 0))
        self.connect((self.uhd_usrp_source, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.uhd_usrp_source, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.uhd_usrp_source, 0), (self.file_sink_source, 0))
        self.connect((self.uhd_usrp_source, 0), (self.fir_filter, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhf_rfid_blocks_analysis")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        with self._lock:
            self.adc_rate = adc_rate
            self.set_samplerate_rfidblocks(self.adc_rate/1)
            self.set_GUI_samples(int(0.7*(44+62+16+62+18+62+96+62)*(self.adc_rate*24/1000000)))
            self.uhd_usrp_source.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_2_1.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_2_0_0.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_2_0.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_2.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_1.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0_0.set_samp_rate(self.adc_rate)
            self.qtgui_time_sink_x_0.set_samp_rate(self.adc_rate)

    def get_tx_gain_antenna(self):
        return self.tx_gain_antenna

    def set_tx_gain_antenna(self, tx_gain_antenna):
        with self._lock:
            self.tx_gain_antenna = tx_gain_antenna

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        with self._lock:
            self.tx_gain = tx_gain
            self.uhd_usrp_sink.set_gain(self.tx_gain, 0)


    def get_taps_fir_averaging_samples(self):
        return self.taps_fir_averaging_samples

    def set_taps_fir_averaging_samples(self, taps_fir_averaging_samples):
        with self._lock:
            self.taps_fir_averaging_samples = taps_fir_averaging_samples
            self.fir_filter.set_taps((self.taps_fir_averaging_samples))

    def get_samplerate_rfidblocks(self):
        return self.samplerate_rfidblocks

    def set_samplerate_rfidblocks(self, samplerate_rfidblocks):
        with self._lock:
            self.samplerate_rfidblocks = samplerate_rfidblocks
            self.qtgui_time_sink_x_0_1_0.set_samp_rate(int(self.samplerate_rfidblocks))
            self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(int(self.samplerate_rfidblocks))

    def get_rx_gain_antenna(self):
        return self.rx_gain_antenna

    def set_rx_gain_antenna(self, rx_gain_antenna):
        with self._lock:
            self.rx_gain_antenna = rx_gain_antenna

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        with self._lock:
            self.rx_gain = rx_gain
            self.uhd_usrp_source.set_gain(self.rx_gain, 0)


    def get_print_results(self):
        return self.print_results

    def set_print_results(self, print_results):
        with self._lock:
            self.print_results = print_results

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        with self._lock:
            self.frequency = frequency
            self.uhd_usrp_source.set_center_freq(self.frequency, 0)
            self.uhd_usrp_sink.set_center_freq(self.frequency, 0)

    def get_dac_rate(self):
        return self.dac_rate

    def set_dac_rate(self, dac_rate):
        with self._lock:
            self.dac_rate = dac_rate
            self.uhd_usrp_sink.set_samp_rate(self.dac_rate)

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        with self._lock:
            self.ampl = ampl
            self.multiply_const_ff.set_k(self.ampl)

    def get_GUI_samples(self):
        return self.GUI_samples

    def set_GUI_samples(self, GUI_samples):
        with self._lock:
            self.GUI_samples = GUI_samples


def main(top_block_cls=uhf_rfid_blocks_analysis, options=None):
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
