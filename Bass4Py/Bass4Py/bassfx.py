from ctypes import *
from .exceptions import *
BOOL=c_long
DWORD=c_ulong
HFX=DWORD
HCHANNEL=DWORD
class BASSFX(object):
 def __init__(self, **kwargs):
  self.__bass=kwargs['bass']
  self._stream=kwargs['stream']
  self._fx=kwargs['fx']
  self.__bass_channelremovefx=self.__bass._bass.BASS_ChannelRemoveFX
  self.__bass_channelremovefx.restype=BOOL
  self.__bass_channelremovefx.argtypes=[HCHANNEL,HFX]
 def __repr__(self):
  return '<BASSFX object at %d; matching handle %d>'%(self._fx,self._stream)
 def Free(self):
  ret_=self.__bass_channelremovefx(self._stream,self._fx)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)