import platform
import sys
import os.path
import types
from ctypes import *
BOOL=c_long
DWORD=c_ulong
HWND=c_void_p
WINFUNCTYPE=CFUNCTYPE
try:
 WindowsError
except:
 WindowsError=None
from constants import *
from basschannel import *
from bassplugin import *
from bassstream import *
from bassmusic import *
from bassversion import *
from basssample import *
from .exceptions import *
BASS_DWORD_ERROR =4294967295
HSTREAM =DWORD
HPLUGIN=DWORD
HMUSIC=DWORD
HRECORD=DWORD
HSAMPLE=DWORD
QWORD=c_longlong
tDownloadProc = WINFUNCTYPE(None, c_void_p, DWORD, c_void_p)
tStreamProc=WINFUNCTYPE(DWORD,HSTREAM,c_void_p,DWORD,c_void_p)
tFileCloseProc=WINFUNCTYPE(None,c_void_p)
tFileLenProc=WINFUNCTYPE(QWORD,c_void_p)
tFileReadProc=WINFUNCTYPE(DWORD,c_void_p,DWORD,c_void_p)
tFileSeekProc=WINFUNCTYPE(BOOL,QWORD,c_void_p)
tRecordProc=WINFUNCTYPE(BOOL,DWORD,c_void_p,DWORD,c_void_p)
__callbackreferences__=[]
class bass_vector(Structure):
 _fields_ =[("X", c_float), ("Y", c_float), ("Z", c_float)]
class bass_deviceinfo(Structure):
 _fields_ = [("name", c_char_p), ("driver", c_char_p), ("flags", DWORD)]
class bass_info(Structure):
    _fields_ = [
        ("flags", DWORD),
        ("hwsize", DWORD),
        ("hwfree", DWORD),
        ("freesam", DWORD),
        ("free3d", DWORD),
        ("minrate", DWORD),
        ("maxrate", DWORD),
        ("eax", BOOL),
        ("minbuf", DWORD),
        ("dsver", DWORD),
        ("latency", DWORD),
        ("initflags", DWORD),
        ("speakers", DWORD),
        ("freq", DWORD),
    ]
class bass_fileprocs(Structure):
 _fields_=[('close',tFileCloseProc),('length',tFileLenProc),('read',tFileReadProc),('seek',tFileSeekProc)]
class bass_recordinfo(Structure):
 _fields_=[('flags',DWORD),('formats',DWORD),('inputs',DWORD),('singlein',BOOL),('freq',DWORD)]
class BASS(object):
 '''
| Parameters:
| LibFile: Path to the library file. Make sure you choose the right library file (x86 and x64). Currently the system knows how to load Windows, Linux and cygwin libraries. The windows library will be accepted when running under cygwin.
| ForceLoad: This parameter defines if to check for the currently supported library version. Default value is False, which means that the initiation method will check the library version and raise an exception if the version doesn't match with the currently supported API version. True will skip this check procedure. But notice that loading a different version than the version this API was written for might cause problems.
 '''
 APIVersion=33819136
 def __init__(self, LibFile, ForceLoad=False):
  self._bass = self.__GetBassLib(LibFile,ForceLoad)
  self.__bass_init = self._bass.BASS_Init
  self.__bass_init.restype = BOOL
  self.__bass_init.argtypes = [c_int, DWORD, DWORD, HWND, c_void_p]
  self.__bass_errorgetcode = self._bass.BASS_ErrorGetCode
  self.__bass_errorgetcode.restype = c_int
  self.__bass_getdeviceinfo = self._bass.BASS_GetDeviceInfo
  self.__bass_getdeviceinfo.restype=BOOL
  self.__bass_getdeviceinfo.argtypes=[DWORD, POINTER(bass_deviceinfo)]
  self.__bass_streamcreateurl = self._bass.BASS_StreamCreateURL
  self.__bass_streamcreateurl.restype = HSTREAM
  self.__bass_streamcreateurl.argtypes =[c_char_p, DWORD, DWORD, tDownloadProc, c_void_p]
  self.__bass_streamcreate=self._bass.BASS_StreamCreate
  self.__bass_streamcreate.restype=HSTREAM
  self.__bass_streamcreate.argtypes=[DWORD,DWORD,DWORD,tStreamProc,c_void_p]
  self.__bass_streamcreatefileuser=self._bass.BASS_StreamCreateFileUser
  self.__bass_streamcreatefileuser.restype=HSTREAM
  self.__bass_streamcreatefileuser.argtypes=[DWORD,DWORD,POINTER(bass_fileprocs),c_void_p]
  self.__bass_setconfig = self._bass.BASS_SetConfig
  self.__bass_setconfig.restype = BOOL
  self.__bass_setconfig.argtypes = [DWORD, DWORD]
  self.__bass_getconfig = self._bass.BASS_GetConfig
  self.__bass_getconfig.restype = DWORD
  self.__bass_getconfig.argtypes = [DWORD]
  self.__bass_getconfigptr=self._bass.BASS_GetConfigPtr
  self.__bass_getconfigptr.restype=c_char_p
  self.__bass_getconfigptr.argtypes=[DWORD]
  self.__bass_setconfigptr=self._bass.BASS_SetConfigPtr
  self.__bass_setconfigptr.restype=BOOL
  self.__bass_setconfigptr.argtypes=[DWORD,c_char_p]
  self.__bass_getversion = self._bass.BASS_GetVersion
  self.__bass_getversion.restype = DWORD
  self.__bass_setdevice = self._bass.BASS_SetDevice
  self.__bass_setdevice.restype = BOOL
  self.__bass_setdevice.argtypes = [DWORD]
  self.__bass_getdevice = self._bass.BASS_GetDevice
  self.__bass_getdevice.restype=DWORD
  self.__bass_free = self._bass.BASS_Free
  self.__bass_free.restype=BOOL
  try:
   self.__bass_seteaxparameters = self._bass.BASS_SetEAXParameters
   self.__bass_seteaxparameters.restype=BOOL
   self.__bass_seteaxparameters.argtypes=[c_int, c_float, c_float, c_float]
   self.__bass_geteaxparameters = self._bass.BASS_GetEAXParameters
   self.__bass_geteaxparameters.restype=BOOL
   self.__bass_geteaxparameters.argtypes=[POINTER(DWORD), POINTER(c_float), POINTER(c_float), POINTER(c_float)]
  except:
   pass
  self.__bass_getinfo = self._bass.BASS_GetInfo
  self.__bass_getinfo.restype = BOOL
  self.__bass_getinfo.argtypes =[POINTER(bass_info)]
  self.__bass_update = self._bass.BASS_Update
  self.__bass_update.restype=BOOL
  self.__bass_update.argtypes=[DWORD]
  self.__bass_getcpu = self._bass.BASS_GetCPU
  self.__bass_getcpu.restype=c_float
  self.__bass_start = self._bass.BASS_Start
  self.__bass_start.restype=BOOL
  self.__bass_stop = self._bass.BASS_Stop
  self.__bass_stop.restype=BOOL
  self.__bass_pause = self._bass.BASS_Pause
  self.__bass_pause.restype=BOOL
  self.__bass_setvolume = self._bass.BASS_SetVolume
  self.__bass_setvolume.restype=BOOL
  self.__bass_setvolume.argtypes=[c_float]
  self.__bass_getvolume=self._bass.BASS_GetVolume
  self.__bass_getvolume.restype=c_float
  self.__bass_pluginload = self._bass.BASS_PluginLoad
  self.__bass_pluginload.restype=HPLUGIN
  self.__bass_pluginload.argtypes=[c_wchar_p, DWORD]
  self.__bass_set3dfactors = self._bass.BASS_Set3DFactors
  self.__bass_set3dfactors.restype=BOOL
  self.__bass_set3dfactors.argtypes=[c_float, c_float, c_float]
  self.__bass_get3dfactors = self._bass.BASS_Get3DFactors
  self.__bass_get3dfactors.restype=BOOL
  self.__bass_get3dfactors.argtypes=[POINTER(c_float), POINTER(c_float), POINTER(c_float)]
  self.__bass_set3dposition = self._bass.BASS_Set3DPosition
  self.__bass_set3dposition.restype=BOOL
  self.__bass_set3dposition.argtypes=[POINTER(bass_vector), POINTER(bass_vector), POINTER(bass_vector), POINTER(bass_vector)]
  self.__bass_get3dposition=self._bass.BASS_Get3DPosition
  self.__bass_get3dposition.restype=BOOL
  self.__bass_get3dposition.argtypes=[POINTER(bass_vector), POINTER(bass_vector), POINTER(bass_vector), POINTER(bass_vector)]
  self.__bass_apply3d = self._bass.BASS_Apply3D
  self.__bass_apply3d.restype=None
  self.__bass_musicload = self._bass.BASS_MusicLoad
  self.__bass_musicload.restype=HMUSIC
  self.__bass_musicload.argtypes=[BOOL, c_void_p, QWORD, DWORD, DWORD, DWORD]
  self.__bass_streamcreatefile=self._bass.BASS_StreamCreateFile
  self.__bass_streamcreatefile.restype=HSTREAM
  self.__bass_streamcreatefile.argtypes=[BOOL,c_void_p,QWORD,QWORD,DWORD]
  self.__bass_samplecreate=self._bass.BASS_SampleCreate
  self.__bass_samplecreate.restype=HSAMPLE
  self.__bass_samplecreate.argtypes=[DWORD,DWORD,DWORD,DWORD,DWORD]
  self.__bass_sampleload=self._bass.BASS_SampleLoad
  self.__bass_sampleload.restype=HSAMPLE
  self.__bass_sampleload.argtypes=[BOOL,c_void_p,QWORD,DWORD,DWORD,DWORD]
  self.__bass_recordinit=self._bass.BASS_RecordInit
  self.__bass_recordinit.restype=BOOL
  self.__bass_recordinit.argtypes=[c_int]
  self.__bass_recordfree=self._bass.BASS_RecordFree
  self.__bass_recordfree.restype=BOOL
  self.__bass_recordgetdevice=self._bass.BASS_RecordGetDevice
  self.__bass_recordgetdevice.restype=DWORD
  self.__bass_recordgetinput=self._bass.BASS_RecordGetInput
  self.__bass_recordgetinput.restype=DWORD
  self.__bass_recordgetinput.argtypes=[c_int,POINTER(c_float)]
  self.__bass_recordgetinputname=self._bass.BASS_RecordGetInputName
  self.__bass_recordgetinputname.restype=c_char_p
  self.__bass_recordgetinputname.argtypes=[c_int]
  self.__bass_recordsetdevice=self._bass.BASS_RecordSetDevice
  self.__bass_recordsetdevice.restype=BOOL
  self.__bass_recordsetdevice.argtypes=[DWORD]
  self.__bass_recordsetinput=self._bass.BASS_RecordSetInput
  self.__bass_recordsetinput.restype=BOOL
  self.__bass_recordsetinput.argtypes=[c_int,DWORD,c_float]
  self.__bass_recordstart=self._bass.BASS_RecordStart
  self.__bass_recordstart.restype=HRECORD
  self.__bass_recordstart.argtypes=[DWORD,DWORD,DWORD,tRecordProc,c_void_p]
  self.__bass_recordgetdeviceinfo=self._bass.BASS_RecordGetDeviceInfo
  self.__bass_recordgetdeviceinfo.restype=BOOL
  self.__bass_recordgetdeviceinfo.argtypes=[DWORD,POINTER(bass_deviceinfo)]
  self.__bass_recordgetinfo=self._bass.BASS_RecordGetInfo
  self.__bass_recordgetinfo.restype=BOOL
  self.__bass_recordgetinfo.argtypes=[POINTER(bass_recordinfo)]
 def Init(self, device=-1, frequency=44100, flags=0, hwnd=0, clsid=0):
  ''' 
| Reference: http://www.un4seen.com/doc/bass/BASS_Init.html
|
| Will initialize an output device for playback.
| Returns True on success, raises exception on failure.
  '''
  result=self.__bass_init(device,frequency,flags,hwnd,clsid)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 @property
 def _Error(self):
  return int(self.__bass_errorgetcode())
 def GetDeviceInfo(self, index=1):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_GetDeviceInfo.html
|
| Retrieves information on an output device.
| Will return a dictionary with the following keys on success, otherwise raise an exception:
| Name: device name
| Driver: Driver information
| Flags: the device's flags
| Take a look at the `structure <http://www.un4seen.com/doc/bass/BASS_DEVICEINFO.html>`_ for more information.
  '''
  bret_ = bass_deviceinfo()
  sret_ = self.__bass_getdeviceinfo(index, bret_)
  if self._Error:
   raise BassExceptionError(self._Error)
  else:
   return {"Name":bret_.name, "Driver":bret_.driver, "Flags":int(bret_.flags)}
 def StreamCreateURL(self, url, offset=0, flags=0, proc=0, user=0):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_StreamCreateURL.html
|
| Creates a :class:`Bass4Py.BASSSTREAM` object for a given url.
  '''
  if type(proc) !=types.FunctionType and proc !=0:
   raise BassParameterError('Invalid proc parameter: It needs to be a valid function or 0 to disable callback')
  tproc=(proc if type(proc)!=types.FunctionType else tDownloadProc(proc))
  args=self.__bass_streamcreateurl.argtypes
  args[3]=(c_int if type(proc)!=types.FunctionType else tDownloadProc)
  self.__bass_streamcreateurl.argtypes=args
  ret_ = self.__bass_streamcreateurl(url, offset, flags, tproc, user)
  if self._Error:
   raise BassExceptionError(self._Error)
  else:
   __callbackreferences__.append(tproc)
   stream = BASSSTREAM(bass=self, stream=ret_)
   return stream
 def StreamCreate(self,freq=44100,chans=2,flags=0,proc=0,user=None):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_StreamCreate.html
|
| Creates a :class:`Bass4Py.BASSSTREAM` object with the given arguments.
  '''
  if type(proc)!=types.FunctionType and proc!=STREAMPROC_DUMMY and proc!=STREAMPROC_PUSH:
   raise BassParameterError('Invalid proc parameter: valid function or STREAMPROC_DUMMY or STREAMPROC_PUSH needed')
  tproc=(proc if type(proc)!=types.FunctionType else tStreamProc(proc))
  args=self.__bass_streamcreate.argtypes
  args[4]=(c_int if type(proc)!=types.FunctionType else tStreamProc)
  self.__bass_streamcreate.argtypes=args
  ret_=self.__bass_streamcreate(freq,chans,flags,tproc,user)
  if self._Error: raise BassExceptionError(self._Error)
  __callbackreferences__.append(tproc)
  stream=BASSSTREAM(bass=self,stream=ret_)
  return stream
 def StreamCreateFileUser(self,system,flags,closeproc,lenproc,readproc,seekproc,user):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_StreamCreateFileUser.html
|
| Creates a :class:`Bass4Py.BASSSTREAM` object for a file with user-defined file handling functions.
  '''
  if type(closeproc)!=types.FunctionType: raise BassParameterError('Invalid closeproc parameter: function type expected')
  if type(lenpoc)!=types.FunctionType: raise BassParameterError('Invalid lenproc parameter: function type expected')
  if type(readproc)!=types.FunctionType: raise BassParameterError('Invalid lenproc parameter: function type expected')
  if type(seekproc)!=types.FunctionType: raise BassParameterError('Invalid seekproc parameter: function type expected')
  proc=bass_fileprocs()
  proc.close=tFileCloseProc(closeproc)
  proc.length=tFileLenProc(lenproc)
  proc.read=tFileReadProc(readproc)
  proc.seek=tFileSeekProc(seekproc)
  ret_=self.__bass_streamcreatefileuser(system,flags,proc,user)
  if self._Error: raise BassExceptionError(self._Error)
  stream=BASSSTREAM(bass=self,stream=ret_)
  return stream
 def __SetConfig(self, option, value):
  result=self.__bass_setconfig(option, value)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def __GetConfig(self, option):
  result=self.__bass_getconfig(option)
  if self._Error: raise BassExceptionError(self._Error)
  return int(result)
 def __GetConfigPtr(self,option):
  ret_=self.__bass_getconfigptr(option)
  if self._Error: raise BassExceptionError(self._Error)
  return ret_
 def __SetConfigPtr(self,option,value):
  ret_=self.__bass_setconfigptr(option,value)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(ret_)
 @property
 def Version(self):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_GetVersion.html
|
| Returns a :class:`Bass4Py.BASSVERSION` object, containing the current API version in integer and string format.
  '''
  dversion=self.__bass_getversion()
  return BASSVERSION(dversion)
 @property
 def Device(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetDevice.html
|             http://www.un4seen.com/doc/bass/BASS_SetDevice.html
|
| When assigning a value:
|                        Sets the currently used device. This will fail if the set device wasn't initialized via :meth:`Bass4Py.BASS.Init` and then raise an exception.
| When retrieving the value:
|                           Returns the currently used device ID or raises an exception on failure.
  '''
  ret_ = self.__bass_getdevice()
  if self._Error: raise BassExceptionError(self._Error)
  return int(ret_)
 @Device.setter
 def Device(self, device):
  result=self.__bass_setdevice(device)
  if self._Error: raise BassExceptionError(self._Error)
 def Free(self):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_Free.html
|
| Frees all BASS channels and uninitializes all devices, doesn't return anything
  '''
  result=self.__bass_free()
  if self._Error: raise BassExceptionError(self._Error)
 def __Info(self):
  bret_ = bass_info()
  sret_ = self.__bass_getinfo(bret_)
  if self._Error: raise BassExceptionError(self._Error)
  return {"flags":bret_.flags,"hwsize":bret_.hwsize,"hwfree":bret_.hwfree,"freesam":bret_.freesam,"free3d":bret_.free3d,"minrate":bret_.minrate,"maxrate":bret_.maxrate,"eax":bret_.eax,"minbuf":bret_.minbuf,"dsver":bret_.dsver,"latency":bret_.latency,"initflags":bret_.initflags,"speakers":bret_.speakers,"freq":bret_.freq}
 @property
 def DeviceFlags(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the device's capabilities
  '''
  return int(self.__Info()['flags'])
 @property
 def DeviceFullMemory(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the device's total amount of memory
  '''
  return int(self.__Info()['hwsize'])
 @property
 def DeviceFreeMemory(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the device's free amount of memory
  '''
  return int(self.__Info()['hwfree'])
 @property
 def FreeSamples(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the number of free samples in the hardware
  '''
  return int(self.__Info()['freesam'])
 @property
 def Free3D(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Number of free 3D slots in the hardware
  '''
  return int(self.__Info()['free3d'])
 @property
 def MinSampleRate(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| The minimum sample rate supported by the hardware
  '''
  return int(self.__Info()['minrate'])
 @property
 def MaxSampleRate(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| The maximum sample rate supported by the hardware
  '''
  return int(self.__Info()['maxrate'])
 @property
 def EAX(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns True if EAX is available, else False
  '''
  return bool(self.__Info()['eax'])
 @property
 def MinBuffer(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| The minimum buffer size possible for configuration (see :attr:`Bass4Py.BASS.Buffer`). If the return value is invalid, a :class:`Bass4Py.BassDWORDError` exception will be raised
  '''
  ret_=self.__Info()['minbuf']
  if ret_==BASS_DWORD_ERROR: raise BassDWORDError()
  return int(ret_)
 @property
 def DirectSoundVersion(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
| Returns the available DirectSound version on windows
  '''
  return int(self.__Info()['dsver'])
 @property
 def Latency(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the latency which occurs between channel start and playback
  '''
  ret_=self.__Info()['latency']
  if ret_==BASS_DWORD_ERROR: raise BassDWORDError()
  return int(ret_)
 @property
 def InitFlags(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the flags used in the :meth:`Bass4Py.BASS.Init` call
  '''
  return int(self.__Info()['initflags'])
 @property
 def Speakers(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the number of available speakers
  '''
  return int(self.__Info()['speakers'])
 @property
 def DeviceFrequency(self):
  '''
| References: http://www.un4seen.com/doc/bass/BASS_GetInfo.html
|             http://www.un4seen.com/doc/bass/BASS_INFO.html
|
| Returns the device's current output sample rate
  '''
  return int(self.__Info()['freq'])
 def Update(self, length):
  '''
| Reference: http://www.un4seen.com/doc/bass/BASS_Update.html
|
| Updates the playback buffers.
| Returns True or raises an exception
  '''
  result=self.__bass_update(length)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 @property
 def CPU(self):
  return self.__bass_getcpu()
 def Start(self):
  result=self.__bass_start()
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def Stop(self):
  result=self.__bass_stop()
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def Pause(self):
  result=self.__bass_pause()
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 @property
 def Volume(self):
  result=self.__bass_getvolume()
  if self._Error: raise BassExceptionError(self._Error)
  return result
 @Volume.setter
 def Volume(self, volume):
  result=self.__bass_setvolume(volume)
  if self._Error: raise BassExceptionError(self._Error)
 def PluginLoad(self, file):
  ret_ = self.__bass_pluginload(file,BASS_UNICODE)
  if self._Error:
   raise BassExceptionError(self._Error)
  return BASSPLUGIN(bass=self, plugin=ret_)
 def __Set3DFactors(self, distf, rollf, doppf):
  result=self.__bass_set3dfactors(distf, rollf, doppf)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def __Get3DFactors(self):
  distf=c_float(0)
  rollf=c_float(0)
  doppf=c_float(0)
  ret_ =self.__bass_get3dfactors(distf, rollf, doppf)
  if self._Error: raise BassExceptionError(self._Error)
  return {"distf":distf.value, "rollf":rollf.value, "doppf":doppf.value}
 @property
 def Distance(self):
  return self.__Get3DFactors()['distf']
 @Distance.setter
 def Distance(self,distance):
  ret_=self.__Get3DFactors()
  self.__Set3DFactors(distance,ret_['rollf'],ret_['doppf'])
  self._Apply3D()
 @property
 def Doppler(self):
  return self.__Get3DFactors()['doppf']
 @Doppler.setter
 def Doppler(self,doppler):
  ret_=self.__Get3DFactors()
  self.__Set3DFactors(ret_['distf'],ret_['rollf'],doppler)
  self._Apply3D()
 @property
 def Rolloff(self):
  return self.__Get3DFactors()['rollf']
 @Rolloff.setter
 def Rolloff(self,rolloff):
  ret_=self.__Get3DFactors()
  self.__Set3DFactors(ret_['distf'],rolloff,ret_['doppf'])
  self._Apply3D()
 def __Set3DPosition(self, pos, vel, front, top):
  if type(pos) is types.DictType:
   bpos = bass_vector()
   bpos.X = pos["X"]
   bpos.Y = pos["Y"]
   bpos.Z = pos["Z"]
  else:
   raise BassParameterError('The position must be in dictionary format.')
  if type(vel) is types.DictType:
   bvel = bass_vector()
   bvel.X = vel["X"]
   bvel.Y = vel["Y"]
   bvel.Z = vel["Z"]
  else:
   raise BassParameterError('The velocity parameter must be in dictionary format.')
  if type(front) is types.DictType:
   bfront = bass_vector()
   bfront.X = front["X"]
   bfront.Y = front["Y"]
   bfront.Z = front["Z"]
  else:
   raise BassParameterError('The front parameter must be in dictionary format.')
  if type(top) is types.DictType:
   btop = bass_vector()
   btop.X = top["X"]
   btop.Y = top["Y"]
   btop.Z = top["Z"]
  else:
   raise BassParameterError('The top parameter must be in dictionary format.')
  result=self.__bass_set3dposition(bpos, bvel, bfront, btop)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def __Get3DPosition(self):
  pos = bass_vector()
  vel = bass_vector()
  front = bass_vector()
  top = bass_vector()
  ret_ = self.__bass_get3dposition(pos, vel, front, top)
  if self._Error: raise BassExceptionError(self._Error)
  return {"pos":{"X":pos.X,"Y":pos.Y,"Z":pos.Z},"vel":{"X":vel.X,"Y":vel.Y,"Z":vel.Z},"front":{"X":front.X,"Y":front.Y,"Z":front.Z},"top":{"X":top.X,"Y":top.Y,"Z":top.Z}}
 @property
 def Position(self):
  return self.__Get3DPosition()['pos']
 @Position.setter
 def Position(self,position):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(pos=position,vel=ret_['vel'],top=ret_['top'],front=ret_['front'])
  self._Apply3D()
 @property
 def Velocity(self):
  return self.__Get3DPosition()['vel']
 @Velocity.setter
 def Velocity(self,velocity):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(pos=ret_['pos'],vel=velocity,top=ret_['top'],front=ret_['front'])
  self._Apply3D()
 @property
 def Top(self):
  return self.__Get3DPosition()['top']
 @Top.setter
 def Top(self,top):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(pos=ret_['pos'],vel=ret_['vel'],top=top,front=ret_['front'])
  self.Apply3D()
 @property
 def Front(self):
  return self.__Get3DPosition()['front']
 @Front.setter
 def Front(self,front):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(pos=ret_['pos'],vel=ret_['vel'],top=ret_['top'],front=front)
  self._Apply3D()
 def _Apply3D(self):
  self.__bass_apply3d()
  if self._Error: raise BassExceptionError(self._Error)
 def __SetEAXParameters(self, env, vol, decay, damp):
  result=self.__bass_seteaxparameters(env, vol, decay, damp)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(result)
 def __GetEAXParameters(self):
  env=DWORD(0)
  vol = c_float(0)
  decay = c_float(0)
  damp = c_float(0)
  ret_ = self.__bass_geteaxparameters(env, vol, decay, damp)
  if self._Error: raise BassExceptionError(self._Error)
  return {"env":env.value,"vol":vol.value,"decay":decay.value,"damp":damp.value}
 @property
 def EAXEnvironment(self):
  if not self.EAX: raise BassEAXError()
  return self.__GetEAXParameters()['env']
 @EAXEnvironment.setter
 def EAXEnvironment(self,environment):
  if not self.EAX: raise BassEAXError()
  ret_=self.__GetEAXParameters()
  self.__SetEAXParameters(environment,ret_['vol'],ret_['decay'],ret_['damp'])
 @property
 def EAXVolume(self):
  if not self.EAX: raise BassEAXError()
  return self.__GetEAXParameters()['vol']
 @EAXVolume.setter
 def EAXVolume(self,volume):
  if not self.EAX: raise BassEAXError()
  ret_=self.__GetEAXParameters()
  self.__SetEAXParameters(ret_['env'],volume,ret_['decay'],ret_['damp'])
 @property
 def EAXDecay(self):
  if not self.EAX: raise BassEAXError()
  return self.__GetEAXParameters()['decay']
 @EAXDecay.setter
 def EAXDecay(self,decay):
  if not self.EAX: raise BassEAXError()
  ret_=self.__GetEAXParameters()
  self.__SetEAXParameters(ret_['env'],ret_['vol'],decay,ret_['damp'])
 @property
 def EAXDamp(self):
  if not self.EAX: raise BassEAXError()
  return self.__GetEAXParameters()['damp']
 @EAXDamp.setter
 def EAXDamp(self,damp):
  if not self.EAX: raise BassEAXError()
  ret_=self.__GetEAXParameters()
  self.__SetEAXParameters(ret_['env'],ret_['vol'],ret_['decay'],damp)
 def MusicLoad(self, mem, file, offset=0, length=0, flags=0, freq=0):
  ret_=self.__bass_musicload(mem, file, offset, length, flags, freq)
  if self._Error: raise BassExceptionError(self._Error)
  return BASSMUSIC(bass=self, music=ret_) 
 def StreamCreateFile(self, mem, file,offset=0,length=0,flags=0):
  if mem and length==0: length=len(file)
  result=self.__bass_streamcreatefile(mem,file,offset,length,flags)
  if self._Error: raise BassExceptionError(self._Error)
  return BASSSTREAM(bass=self,stream=result)
 def __GetBassLib(self, LibFile,ForceLoad):
  if platform.system()=='Windows':
   try:
    lib=windll.LoadLibrary(LibFile)
   except WindowsError,e:
    raise BassLibError('Unable to load library %s: %s'%(LibFile,e))
  elif platform.system()=='Linux' or platform.system().startswith('CYGWIN'):
   try:
    lib=CDLL(LibFile)
   except OSError,e:
    raise BassLibError('Unable to load library %s: %s'%(LibFile,e))
  else:
   raise BassLibError('The current system platform \'%s\' is unknown. Please notify the developers about this problem'%system.platform())
  if not ForceLoad:
   versionfunc=lib.BASS_GetVersion
   versionfunc.restype=DWORD
   if versionfunc()!=self.APIVersion:
    raise BassLibError('Your library version doesn\'t match the version number this API is designed for. This can cause problems. If you want to load this API with your current library anyway, call the library creation with the ForceLoad parameter set to True')
  return lib
 def __repr__(self):
  return '<BASS (v%s %s) object interface>'%(self.Version.Str,'x64' if sys.maxsize>2**32 else 'x86')
 def ReceiveStream(self,id):
  return BASSSTREAM(bass=self,stream=id)
 def ReceiveMusic(self,id):
  return BASSMUSIC(bass=self,music=id)
 def ReceiveSample(self,id):
  return BASSSAMPLE(bass=self,stream=id)
 def SampleCreate(self,length,freq,chans,max,flags):
  ret_=self.__bass_samplecreate(length,freq,chans,max,flags)
  if self._Error: raise BassExceptionError(self._Error)
  sample=BASSSAMPLE(bass=self,stream=ret_)
  return sample
 def SampleLoad(self,mem,file,offset=0,length=0,max=65535,flags=0):
  if mem and length==0: length=len(file)
  result=self.__bass_sampleload(mem,file,offset,length,max,flags)
  if self._Error: raise BassExceptionError(self._Error)
  return BASSSAMPLE(bass=self,stream=result)
 def ReceiveChannel(self,id):
  return BASSCHANNEL(bass=self,stream=id)
 def RecordInit(self,device):
  ret_=self.__bass_recordinit(device)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(ret_)
 def RecordFree(self):
  ret_=self.__bass_recordfree()
  if self._Error: raise BassExceptionError(self._Error)
  return bool(ret_)
 @property
 def RecordDevice(self):
  ret_=self.__bass_recordgetdevice()
  if self._Error: raise BassExceptionError(self._Error)
  return int(ret_)
 @RecordDevice.setter
 def RecordDevice(self,device):
  ret_=self.__bass_recordsetdevice(device)
  if self._Error: raise BassExceptionError(self._Error)
 def RecordGetInput(self,input):
  vol=c_float(0)
  ret_=self.__bass_recordgetinput(input,vol)
  if self._Error: raise BassExceptionError(self._Error)
  return (int(ret_),vol.value)
 def RecordGetInputName(self,input):
  ret_=self.__bass_recordgetinputname(input)
  if self._Error: raise BassExceptionError(self._Error)
  return ret_
 def RecordSetInput(self,input,flags,volume):
  ret_=self.__bass_recordsetinput(input,flags,volume)
  if self._Error: raise BassExceptionError(self._Error)
  return bool(ret_)
 def RecordStart(self,freq,chans,flags,proc=0,user=0):
  if proc!=0 and type(proc)!=types.FunctionType: raise BassParameterError('The proc parameter needs to be a valid function or 0 to not define a proc')
  tproc=(proc if type(proc)!=types.FunctionType else tRecordProc(proc))
  args=self.__bass_recordstart.argtypes
  args[3]=(c_int if type(proc)!=types.FunctionType else tRecordProc)
  self.__bass_recordstart.argtypes=args
  ret_=self.__bass_recordstart(freq,chans,flags,tproc,user)
  if self._Error: raise BassExceptionError(self._Error)
  __callbackreferences__.append(tproc)
  return BASSCHANNEL(bass=self,stream=ret_)
 def RecordGetDeviceInfo(self,device):
  bret_=bass_deviceinfo()
  ret_=self.__bass_recordgetdeviceinfo(device,bret_)
  if self._Error: raise BassExceptionError(self._Error)
  return {"Name":bret_.name, "Driver":bret_.driver, "Flags":int(bret_.flags)}
 def __RecordGetInfo(self):
  bret_=bass_recordinfo()
  ret_=self.__bass_recordgetinfo(bret_)
  if self._Error: raise BassExceptionError(self._Error)
  return bret_
 @property
 def RecordDeviceFlags(self):
  return int(self.__RecordGetInfo().flags)
 @property
 def RecordDeviceFormats(self):
  return int(self.__RecordGetInfo().formats)
 @property
 def RecordDeviceInputs(self):
  return int(self.__RecordGetInfo().inputs)
 @property
 def RecordDeviceSingleIn(self):
  return bool(self.__RecordGetInfo().singlein)
 @property
 def RecordDeviceFrequency(self):
  return int(self.__RecordGetInfo().freq)
 @property
 def Algorithm3D(self):
  return self.__GetConfig(BASS_CONFIG_3DALGORITHM)
 @Algorithm3D.setter
 def Algorithm3D(self,val):
  self.__SetConfig(BASS_CONFIG_3DALGORITHM,val)
 @property
 def AsyncFileBuffer(self):
  return self.__GetConfig(BASS_CONFIG_ASYNCFILE_BUFFER)
 @AsyncFileBuffer.setter
 def AsyncFileBuffer(self,val):
  self.__SetConfig(BASS_CONFIG_ASYNCFILE_BUFFER,val)
 @property
 def Buffer(self):
  return self.__GetConfig(BASS_CONFIG_BUFFER)
 @Buffer.setter
 def Buffer(self,val):
  self.__SetConfig(BASS_CONFIG_BUFFER,val)
 @property
 def VolumeCurve(self):
  return bool(self.__GetConfig(BASS_CONFIG_CURVE_VOL))
 @VolumeCurve.setter
 def VolumeCurve(self,val):
  self.__SetConfig(BASS_CONFIG_CURVE_VOL,val)
 @property
 def PanningCurve(self):
  return bool(self.__GetConfig(BASS_CONFIG_CURVE_PAN))
 @PanningCurve.setter
 def PanningCurve(self,val):
  self.__SetConfig(BASS_CONFIG_CURVE_PAN,val)
 @property
 def DeviceBuffer(self):
  return self.__GetConfig(BASS_CONFIG_DEV_BUFFER)
 @DeviceBuffer.setter
 def DeviceBuffer(self,val):
  return self.__SetConfig(BASS_CONFIG_DEV_BUFFER,val)
 @property
 def DefaultDevice(self):
  return bool(self.__GetConfig(BASS_CONFIG_DEV_DEFAULT))
 @DefaultDevice.setter
 def DefaultDevice(self,val):
  self.__SetConfig(BASS_CONFIG_DEV_DEFAULT,val)
 @property
 def FloatDSP(self):
  return bool(self.__GetConfig(BASS_CONFIG_FLOATDSP))
 @FloatDSP.setter
 def FloatDSP(self,val):
  self.__SetConfig(BASS_CONFIG_FLOATDSP,val)
 @property
 def VolumeMusic(self):
  return self.__GetConfig(BASS_CONFIG_GVOL_MUSIC)
 @VolumeMusic.setter
 def VolumeMusic(self,val):
  self.__SetConfig(BASS_CONFIG_GVOL_MUSIC,val)
 @property
 def VolumeSample(self):
  return self.__GetConfig(BASS_CONFIG_GVOL_SAMPLE)
 @VolumeSample.setter
 def VolumeSample(self,val):
  self.__SetConfig(BASS_CONFIG_GVOL_SAMPLE,val)
 @property
 def VolumeStream(self):
  return self.__GetConfig(BASS_CONFIG_GVOL_STREAM)
 @VolumeStream.setter
 def VolumeStream(self,val):
  self.__SetConfig(BASS_CONFIG_GVOL_STREAM,val)
 @property
 def VirtualMusicChannels(self):
  return self.__GetConfig(BASS_CONFIG_MUSIC_VIRTUAL)
 @VirtualMusicChannels.setter
 def VirtualMusicChannels(self,val):
  self.__SetConfig(BASS_CONFIG_MUSIC_VIRTUAL,val)
 @property
 def UserAgent(self):
  return self.__GetConfigPtr(BASS_CONFIG_NET_AGENT)
 @UserAgent.setter
 def UserAgent(self,val):
  self.__SetConfigPtr(BASS_CONFIG_NET_AGENT,val)
 @property
 def NetBuffer(self):
  return self.__GetConfig(BASS_CONFIG_NET_BUFFER)
 @NetBuffer.setter
 def NetBuffer(self,val):
  self.__SetConfigPtr(BASS_CONFIG_NET_BUFFER,val)
 @property
 def PassiveFTP(self):
  return bool(self.__GetConfig(BASS_CONFIG_NET_PASSIVE))
 @PassiveFTP.setter
 def PassiveFTP(self,val):
  self.__SetConfig(BASS_CONFIG_NET_PASSIVE,val)
 @property
 def Playlist(self):
  return self.__GetConfig(BASS_CONFIG_NET_PLAYLIST)
 @Playlist.setter
 def Playlist(self,val):
  self.__SetConfig(BASS_CONFIG_NET_PLAYLIST,val)
 @property
 def PreBuffer(self):
  return self.__GetConfig(BASS_CONFIG_NET_PREBUF)
 @PreBuffer.setter
 def PreBuffer(self,val):
  self.__SetConfig(BASS_CONFIG_NET_PREBUF,val)
 @property
 def Proxy(self):
  return self.__GetConfigPtr(BASS_CONFIG_NET_PROXY)
 @Proxy.setter
 def Proxy(self,val):
  self.__SetConfigPtr(BASS_CONFIG_NET_PROXY,val)
 @property
 def NetReadTimeout(self):
  return self.__GetConfig(BASS_CONFIG_NET_READTIMEOUT)
 @NetReadTimeout.setter
 def NetReadTimeout(self,val):
  self.__SetConfig(BASS_CONFIG_NET_READTIMEOUT,val)
 @property
 def NetTimeout(self):
  return self.__GetConfig(BASS_CONFIG_NET_TIMEOUT)
 @NetTimeout.setter
 def NetTimeout(self,val):
  self.__SetConfig(BASS_CONFIG_NET_TIMEOUT,val)
 @property
 def OggPrescan(self):
  return bool(self.__GetConfig(BASS_CONFIG_OGG_PRESCAN))
 @OggPrescan.setter
 def OggPrescan(self,val):
  self.__SetConfig(BASS_CONFIG_OGG_PRESCAN,val)
 @property
 def PauseNoPlay(self):
  return bool(self.__GetConfig(BASS_CONFIG_PAUSE_NOPLAY))
 @PauseNoPlay.setter
 def PauseNoPlay(self,val):
  self.__SetConfig(BASS_CONFIG_PAUSE_NOPLAY,val)
 @property
 def RecordBuffer(self):
  return self.__GetConfig(BASS_CONFIG_REC_BUFFER)
 @RecordBuffer.setter
 def RecordBuffer(self,val):
  self.__SetConfig(BASS_CONFIG_REC_BUFFER,val)
 @property
 def SRC(self):
  return self.__GetConfig(BASS_CONFIG_SRC)
 @SRC.setter
 def SRC(self,val):
  self.__SetConfig(BASS_CONFIG_SRC,val)
 @property
 def SRCSample(self):
  return self.__GetConfig(BASS_CONFIG_SRC_SAMPLE)
 @SRCSample.setter
 def SRCSample(self,val):
  self.__SetConfig(BASS_CONFIG_SRC_SAMPLE,val)
 @property
 def DeviceUnicode(self):
  return bool(self.__GetConfig(BASS_CONFIG_UNICODE))
 @DeviceUnicode.setter
 def DeviceUnicode(self,val):
  self.__SetConfig(BASS_CONFIG_UNICODE,val)
 @property
 def UpdatePeriod(self):
  return self.__GetConfig(BASS_CONFIG_UPDATEPERIOD)
 @UpdatePeriod.setter
 def UpdatePeriod(self,val):
  self.__SetConfig(BASS_CONFIG_UPDATEPERIOD,val)
 @property
 def UpdateThreads(self):
  return self.__GetConfig(BASS_CONFIG_UPDATETHREADS)
 @UpdateThreads.setter
 def UpdateThreads(self,val):
  self.__SetConfig(BASS_CONFIG_UPDATETHREADS,val)
 @property
 def Verify(self):
  return self.__GetConfig(BASS_CONFIG_VERIFY)
 @Verify.setter
 def Verify(self,val):
  self.__SetConfig(BASS_CONFIG_VERIFY,val)
 @property
 def VistaSpeakers(self):
  return bool(self.__GetConfig(BASS_CONFIG_VISTA_SPEAKERS))
 @VistaSpeakers.setter
 def VistaSpeakers(self,val):
  self.__SetConfig(BASS_CONFIG_VISTA_SPEAKERS,val)