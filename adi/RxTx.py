import numpy as np
from adi.DDS import DDS
from adi.Attribute import Attribute
from scipy import signal
import sys
import iio

class Phy(Attribute):
    ctrl = []

    def __del__(self):
        self.ctrl = []

class Rx(Attribute):
    rxadc = []
    rx_channel_names = []
    rx_buffer_size = 1024
    rxbuf = None
    rx_channel_mapping = []

    def __del__(self):
        self.rxbuf = []
        self.rxadc = []

    def init_channels(self):
        if self.complex_data:
            for map in self.rx_channel_mapping:
                v = self.rxadc.find_channel(self.rx_channel_names[map*2])
                v.enabled = True
                v = self.rxadc.find_channel(self.rx_channel_names[map*2+1])
                v.enabled = True
        else:
            for map in self.rx_channel_mapping:
                v = self.rxadc.find_channel(self.rx_channel_names[map])
                v.enabled = True
        self.rxbuf = iio.Buffer(self.rxadc, self.rx_buffer_size, False)

    def rx_complex(self):
        if not self.rxbuf:
            self.init_channels(False)
        self.rxbuf.refill()
        data = self.rxbuf.read()
        x = np.frombuffer(data,dtype=np.int16)
        indx = 0
        sig = []
        for c in range(int(self.num_rx_channels/2)):
            sig.append(x[indx::self.num_rx_channels] + 1j*x[indx+1::self.num_rx_channels])
            indx = indx + 2
        return sig

    def rx_non_complex(self):
        if not self.rxbuf:
            self.init_channels(False)
        self.rxbuf.refill()
        data = self.rxbuf.read()
        x = np.frombuffer(data,dtype=np.int16)
        indx = 0
        sig = []
        for c in range(self.num_rx_channels):
            sig.append(x[c::self.num_rx_channels])
        return sig

    def rx(self):
        if self.complex_data:
            return self.rx_complex()
        else:
            return self.rx_non_complex()

class Tx(DDS,Attribute):
    txdac = []
    tx_channel_names = []
    tx_buffer_size = 1024
    tx_cyclic_buffer = False
    txbuf = None
    tx_channel_mapping = []

    def __init__(self):
        DDS.__init__(self)

    def __del__(self):
        self.txdac = []

    def init_channels(self):
        if self.complex_data:
            for map in self.tx_channel_mapping:
                v = self.txdac.find_channel(self.tx_channel_names[map*2],True)
                v.enabled = True
                v = self.txdac.find_channel(self.tx_channel_names[map*2+1],True)
                v.enabled = True
        else:
            for map in self.tx_channel_mapping:
                v = self.txdac.find_channel(self.tx_channel_names[map])
                v.enabled = True
        self.txbuf = iio.Buffer(self.txdac, self.tx_buffer_size, self.tx_cyclic_buffer)

    def tx(self,data):
        if self.complex_data:
            i = np.real(data)
            q = np.imag(data)
            iq = np.empty((i.size + q.size,), dtype=i.dtype)
            iq[0::2] = i
            iq[1::2] = q
            data = np.int16(iq)
        if not self.txbuf:
            self.disable_dds()
            self.tx_buff_length = len(data)
            self.init_channels(True)
        if len(data) != self.tx_buff_length:
            raise
        # Send data to buffer
        self.txbuf.write(data)
        self.txbuf.push()

class RxTx(Rx,Tx,Phy):

    complex_data = False

    def __init__(self):
        print(self.rx_channel_mapping)
        self.num_rx_channels = len(self.rx_channel_names)
        if self.complex_data:
            if max(self.rx_channel_mapping) > ((self.num_rx_channels)/2 - 1):
                raise Exception("RX mapping exceeds available channels")
        else:
            if max(self.rx_channel_mapping) > ((self.num_rx_channels) - 1):
                raise Exception("RX mapping exceeds available channels")
        self.num_tx_channels = len(self.tx_channel_names)
        if self.complex_data:
            if max(self.tx_channel_mapping) > ((self.num_tx_channels)/2 - 1):
                raise Exception("TX mapping exceeds available channels")
        else:
            if max(self.tx_channel_mapping) > ((self.num_tx_channels) - 1):
                raise Exception("TX mapping exceeds available channels")
        Tx.__init__(self)

    def __del__(self):
        Rx.__del__(self)
        Tx.__del__(self)
        Phy.__del__(self)

    def init_channels(self, istx = False):
        if istx:
            Tx.init_channels(self)
        else:
            Rx.init_channels(self)
