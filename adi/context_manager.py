from __future__ import print_function
import sys
import iio

class context_manager(object):
    uri = ''
    def __init__(self, uri="", device_name=""):
        self.uri = uri
        try:
          if self.uri == '':
              contexts = iio.scan_contexts()
              for c in contexts:
                  if device_name in contexts[c]:
                      self.ctx = iio.Context(c)
                      break
          else:
              self.ctx = iio.Context(self.uri)
        except:
          raise Exception("No device found")
