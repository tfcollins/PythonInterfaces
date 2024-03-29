from __future__ import print_function

import logging

import unittest
import numpy as np
from adi import Pluto
import iio

class TestPluto(unittest.TestCase):

    do_plots = False

    def freq_est(self,y,fs):
        N = len(y)
        T = 1.0 / fs
        yf = np.fft.fft(y)
        yf = np.fft.fftshift(yf)
        xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
        if self.do_plots:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot(xf, 2.0/N * np.abs(yf))
            plt.show()
        indx = np.argmax(np.abs(yf))
        return xf[indx]


    def setUp(self):
        self.longMessage = True

    def tearDown(self):
        pass

    def testPlutoADC(self):
        # See if we can get non-zero data from Pluto
        sdr = Pluto()
        data = sdr.rx()
        s = np.sum(np.abs(data))
        self.assertGreater(s,0,'check non-zero data')

    def testPlutoDAC(self):
        # See if we can tone from Pluto using DMAs
        sdr = Pluto()
        sdr.tx_lo = 1000000000
        sdr.rx_lo = 1000000000
        sdr.tx_cyclic_buffer = True
        sdr.tx_hardwaregain = -30
        sdr.gain_control_mode = 'slow_attack'
        sdr.rx_buffer_size = 2**20
        # Create a sinewave waveform
        RXFS = int(sdr.sample_rate)
        fc = RXFS*0.1
        N = 2**15
        ts = 1/float(RXFS)
        t = np.arange(0, N*ts, ts)
        i = np.cos(2*np.pi*t*fc) * 2**15 * 0.5
        q = np.sin(2*np.pi*t*fc) * 2**15 * 0.5
        iq = i + 1j*q
        # Pass through SDR
        sdr.tx(iq)
        for k in range(5):
            data = sdr.rx()

        tone_freq = self.freq_est(data,RXFS)

        if self.do_plots:
            import matplotlib.pyplot as plt
            reals = np.real(data)
            plt.plot(reals)
            imags = np.imag(data)
            plt.plot(imags)
            plt.xlabel("Samples")
            plt.ylabel("Amplitude [dbFS]")
            plt.show()

        diff = np.abs(tone_freq - fc)
        self.assertGreater(fc*0.01,diff,'Frequency offset')

if __name__=='__main__':
    from os import path
    import sys
    try:
        iio.Context('ip:192.168.2.1')
    except:
        print('No Pluto found')
        sys.exit(1)
    unittest.main()
