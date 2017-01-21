from ctypes import *
from .exceptions import *
from bassversion import *
BOOL=c_long
DWORD=c_ulong
HPLUGIN=DWORD
class bass_pluginform(Structure):
    _fields_ = [
        ("ctype", DWORD),
        ("name", c_char_p),
        ("exts", c_char_p)
    ]
class bass_plugininfo(Structure):
    _fields_ = [
        ("version", DWORD),
        ("formatc", DWORD),
        ("formats", POINTER(bass_pluginform))
    ]
class BASSPLUGIN(object):
 def __init__(self, **kwargs):
  self.__bass = kwargs['bass']
  self._plugin = kwargs['plugin']
  self.__bass_pluginfree = self.__bass._bass.BASS_PluginFree
  self.__bass_pluginfree.restype=BOOL
  self.__bass_pluginfree.argtypes=[HPLUGIN]
  self.__bass_plugingetinfo = self.__bass._bass.BASS_PluginGetInfo
  self.__bass_plugingetinfo.restype=c_void_p
  self.__bass_plugingetinfo.argtypes=[HPLUGIN]
 def Free(self):
  ret_=self.__bass_pluginfree(self._plugin)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)
 def __Info(self):
  ret_ = self.__bass_plugingetinfo(self._plugin)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  dret_ ={}
  ret_ = cast(ret_, POINTER(bass_plugininfo))
  ret_ = ret_.contents
  dret_["version"] = BASSVERSION(ret_.version)
  formats =[]
  for i in range(ret_.formatc):
   form ={}
   form["Type"] = int(ret_.formats[i].ctype)
   form["Name"] = ret_.formats[i].name
   form["Extensions"] = ret_.formats[i].exts
   formats.append(form)
  dret_["formats"] = formats
  return dret_
 @property
 def Version(self):
  return self.__Info()['version']
 @property
 def Formats(self):
  return self.__Info()['formats']
 def __repr__(self):
  return '<BASSPLUGIN object at %s>'%(self._plugin)