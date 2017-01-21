from ctypes import *
from .exceptions import *
BOOL=c_long
DWORD=c_ulong
HCHANNEL=DWORD
HDSP=DWORD
class BASSDSP(object):
 def __init__(self, **kwargs):
  self.__bass=kwargs['bass']
  self._stream=kwargs['stream']
  self._dsp=kwargs['dsp']
  self.__bass_channelremovedsp=self.__bass._bass.BASS_ChannelRemoveDSP
  self.__bass_channelremovedsp.restype=BOOL
  self.__bass_channelremovedsp.argtypes=[HCHANNEL,HDSP]
 def __repr__(self):
  return '<BASSDSP object at %d; matching handle %d>'%(self._dsp,self._stream)
 def Free(self):
  ret_=self.__bass_channelremovedsp(self._stream,self._dsp)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)