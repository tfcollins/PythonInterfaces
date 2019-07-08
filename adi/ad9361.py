
from adi.rx_tx import rx_tx
from adi.context_manager import context_manager

class ad9361(rx_tx,context_manager):
    """ AD9361 Transceiver """
    complex_data = True
    rx_channel_names = ['voltage0','voltage1','voltage2','voltage3']
    tx_channel_names = ['voltage0','voltage1','voltage2','voltage3']
    device_name = ""
    rx_channel_mapping=[0,1]
    tx_channel_mapping=[0,1]

    def __init__(self,uri=""):

        context_manager.__init__(self, uri, self.device_name)

        self.ctrl = self.ctx.find_device("ad9361-phy")
        self.rxadc = self.ctx.find_device("cf-ad9361-lpc")
        self.txdac = self.ctx.find_device("cf-ad9361-dds-core-lpc")

        rx_tx.__init__(self)


    @property
    def gain_control_mode(self):
        """gain_control_mode: Mode of receive path AGC. Options are:
        slow_attack, fast_attack, manual"""
        return self.get_iio_attr("voltage0","gain_control_mode",False)

    @gain_control_mode.setter
    def gain_control_mode(self,value):
        self.set_iio_attr_str("voltage0","gain_control_mode",False,value)

    @property
    def rx_hardwaregain(self):
        """rx_hardwaregain: Gain applied to RX path. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self.get_iio_attr("voltage0","hardwaregain",False)

    @rx_hardwaregain.setter
    def rx_hardwaregain(self,value):
        if self.gain_control_mode == 'manual':
            self.set_iio_attr("voltage0","hardwaregain",False,value)

    @property
    def tx_hardwaregain(self):
        """tx_hardwaregain: Attenuation applied to TX path"""
        return self.get_iio_attr("voltage0","hardwaregain",True)

    @tx_hardwaregain.setter
    def tx_hardwaregain(self,value):
        self.set_iio_attr("voltage0","hardwaregain",True,value)

    @property
    def rx_rf_bandwidth(self):
        """rx_rf_bandwidth: Bandwidth of front-end analog filter of RX path"""
        return self.get_iio_attr("voltage0","rf_bandwidth",False)

    @rx_rf_bandwidth.setter
    def rx_rf_bandwidth(self,value):
        self.set_iio_attr("voltage0","rf_bandwidth",False,value)

    @property
    def tx_rf_bandwidth(self):
        """tx_rf_bandwidth: Bandwidth of front-end analog filter of TX path"""
        return self.get_iio_attr("voltage0","rf_bandwidth",True)

    @tx_rf_bandwidth.setter
    def tx_rf_bandwidth(self,value):
        self.set_iio_attr("voltage0","rf_bandwidth",True,value)

    @property
    def sample_rate(self):
        """sample_rate: Sample rate RX and TX paths in samples per second"""
        return self.get_iio_attr("voltage0","sampling_frequency",False)

    @sample_rate.setter
    def sample_rate(self,value):
        self.set_iio_attr("voltage0","sampling_frequency",False,value)

    @property
    def rx_lo(self):
        """rx_lo: Carrier frequency of RX path"""
        return self.get_iio_attr("altvoltage0","frequency",True)

    @rx_lo.setter
    def rx_lo(self,value):
        self.set_iio_attr("altvoltage0","frequency",True,value)

    @property
    def tx_lo(self):
        """tx_lo: Carrier frequency of TX path"""
        return self.get_iio_attr("altvoltage1","frequency",True)

    @tx_lo.setter
    def tx_lo(self,value):
        self.set_iio_attr("altvoltage1","frequency",True,value)

class ad9364(ad9361):
    """ AD9364 Transceiver """
    rx_channel_names = ['voltage0','voltage1']
    tx_channel_names = ['voltage0','voltage1']
    rx_channel_mapping=[0]
    tx_channel_mapping=[0]

class ad9363(ad9361):
    """ AD9363 Transceiver """
    pass
