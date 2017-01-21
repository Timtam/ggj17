from ctypes import *
from .exceptions import *
BOOL=c_long
DWORD=c_ulong
HSYNC=DWORD
HCHANNEL=DWORD
class BASSSYNC(object):
 def __init__(self, **kwargs):
  self.__bass=kwargs['bass']
  self._stream=kwargs['stream']
  self._sync=kwargs['sync']
  self.__bass_channelremovesync=self.__bass._bass.BASS_ChannelRemoveSync
  self.__bass_channelremovesync.restype=BOOL
  self.__bass_channelremovesync.argtypes=[HCHANNEL,HSYNC]
 def __repr__(self):
  return '<BASSSYNC object at %d; matching handle %d>'%(self._sync,self._stream)
 def Free(self):
  ret_=self.__bass_channelremovesync(self._stream,self._sync)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)