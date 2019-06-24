import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time

# Create radio
sdr = adi.Pluto()

# Configure properties
sdr.rx_rf_bandwidth = 4000000
sdr.rx_lo = 2000000000
sdr.tx_lo = 2000000000

# Read properties
print("RX LO %s" % (sdr.rx_lo))

# Create a sinewave waveform
RXFS = int(sdr.sample_rate)
fc = 10000
N = 1024
ts = 1/float(RXFS)
t = np.arange(0, N*ts, ts)
i = np.sin(2*np.pi*t*fc) * 2**14
q = np.cos(2*np.pi*t*fc) * 2**14
iq = np.empty((i.size + q.size,), dtype=i.dtype)
iq[0::2] = i
iq[1::2] = q
iq = np.int16(iq)

# sdr.tx(iq)
fs = RXFS
# Collect data
# fs = int(sdr.sample_rate)
for r in range(20):
    # x = sdr.rx2()
    x = sdr.rx()
    f, Pxx_den = signal.periodogram(x[0], fs)
    plt.clf()
    plt.semilogy(f, Pxx_den)
    plt.ylim([1e-7, 1e2])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.draw()
    plt.pause(0.05)
    time.sleep(0.1)

plt.show()