# Gen2 UHF RFID Reader
This is a Gen2 UHF RFID Reader project for GNURadio. It is able to identify commercial Gen2 RFID Tags with FM0 line coding and 40kHz data rate (BLF), and extract their EPC. It requires USRPN200 and a RFX900 or SBX daughterboard.  

The project is based on the UHF RFID Gen2 Reader project available at (https://github.com/nkargas/Gen2-UHF-RFID-Reader).

### Custom GNU Radio Blocks in this project:

- Gate : Responsible for reader command detection.  
- Tag decoder : Responsible for frame synchronization, channel estimation, symbol period estimation and detection.  
- Reader : Create/send reader commands.

## Installation of

- install log4cpp (http://log4cpp.sourceforge.net/)
- install UHD driver + GNU Radio using **wget http://www.sbrac.org/files/build-gnuradio && chmod a+x ./build-gnuradio && ./build-gnuradio**
- cd Gen2-UHF-RFID-Reader/gr-rfid/  
- mkdir build  
- cd build/  
- cmake ../ (logging should be enabled)  
- sudo make install  
- sudo ldconfig  

## Configuration

- Set USRPN210 address in apps/reader.py (default: 192.168.10.2)
- Set frequency in apps/reader.py (default: 865.7e6 MHz)
- Set tx amplitude in apps/reader.py (default: 0.9)
- Set rx gain in apps/reader.py (default: 20)
- Set maximum number of queries in include/global_vars.h (default:1000)
- Set number of inventory round slots in include/global_vars.h (default: 0)

## How to run

- Real time execution:  
If you use an SBX daughterboard uncomment  #self.source.set_auto_dc_offset(False) in reader.py file
cd Gen2-UHF-RFID-Reader/gr-rfid/apps/    
sudo GR_SCHEDULER=STS nice -n -20 python ./reader.py     
After termination, part of EPC message (last 60 bits) of identified Tags are printed.  
 
## Logging

- Configuration file : /home/username/.gnuradio/config.conf  
    Edit the above file and add the following lines  

    [LOG]  
    debug_file = /PathToLogFile/Filename  
    debug_level = info  
    
    Logging may cause latency issues if it is enabled during real time execution!

## Debugging  

The reader may fail to decode a tag response for the following reasons

1) Latency: For real time execution you should disable the output on the terminal. If you see debug messages, you should either install log4cpp or comment the corresponding lines in the source code e.g., GR_LOG_INFO(d_debug_logger, "EPC FAIL TO DECODE");

2) Antenna placement. Place the antennas side by side with a distance of 50-100cm between them and the tag 2m (it can detect a tag up to 6m) away facing the antennas.

3) Parameter tuning. The most important is self.ampl which controls the power of the transmitted signal (takes values between 0 and 1).

If the reader still fails to decode tag responses, uncomment the following line in reader.py file

 #self.connect(self.source, self.file_sink_source)

Run the software for a few seconds (~5s). A file will be created in misc/data directory named source. This file contains the received samples. You can plot the amplitude of the received samples using the script located in misc/code folder. The figure should be similar to the .eps figure included in the folder. Plotting the figure can give some indication regarding the problem. You can also plot the output of any block by uncommenting the corresponding line in the reader.py file. Output files will be created in misc/data folder:

- /misc/data/source  
- /misc/data/matched_filter  
- /misc/data/gate 
- /misc/data/decoder  
- /misc/data/reader

Useful discussions on software issues:

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/1

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/4

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/10

    
## Hardware:

  - 1x Ettus/NI USRPN210  
  - 1x Ettus/NI UBX40 daughterboard  
  - 2x circular polarized antennas  

## Tested on:
  Kuuntu 18.04 64-bit  
  GNU Radio 3.7.11


## Forked from:
N. Kargas, F. Mavromatis and A. Bletsas, "Fully-Coherent Reader with Commodity SDR for Gen2 FM0 and Computational RFID", IEEE Wireless Communications Letters (WCL), Vol. 4, No. 6, pp. 617-620, Dec. 2015. 

## This repository contact:
  (email: diamantx@gmail.com)  