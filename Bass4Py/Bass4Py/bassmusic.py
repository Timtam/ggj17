from ctypes import *
from .exceptions import *
from basschannel import *
BOOL=c_long
DWORD=c_ulong
HMUSIC=DWORD
class BASSMUSIC(object):
 def __init__(self, **kwargs):
  self.__bass = kwargs['bass']
  self._stream = kwargs['stream']
  self.__bass_musicfree = self.__bass._bass.BASS_MusicFree
  self.__bass_musicfree.restype=BOOL
  self.__bass_musicfree.argtypes=[HMUSIC]
 def Free(self):
  ret_=self.__bass_musicfree(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)
 @property
 def Channel(self):
  return BASSCHANNEL(bass=self.__bass, stream=self._stream)
 def __repr__(self):
  return '<BASSMUSIC object at %s>'%(self._stream)