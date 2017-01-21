from ctypes import *
import types
from .exceptions import *
from .constants import *
from basssample import *
from bassplugin import *
from bassdsp import *
from bassfx import *
from basssync import *
BOOL=c_long
DWORD=c_ulong
HWND=c_void_p
WINFUNCTYPE=CFUNCTYPE
QWORD=c_longlong
HCHANNEL=DWORD
HSAMPLE=DWORD
HPLUGIN=DWORD
HFX=DWORD
HSYNC=DWORD
HDSP=DWORD
tDspProc=WINFUNCTYPE(None,DWORD,DWORD,c_void_p,DWORD,c_void_p)
tSyncProc=WINFUNCTYPE(None,DWORD,DWORD,DWORD,c_void_p)
__callbackreferences__=[]
class bass_vector(Structure):
 _fields_ =[("X", c_float), ("Y", c_float), ("Z", c_float)]
class bass_channelinfo(Structure):
    _fields_ = [
        ("freq", DWORD),
        ("chans", DWORD),
        ("flags", DWORD),
        ("ctype", DWORD),
        ("origres", DWORD),
        ("plugin", HPLUGIN),
        ("sample", HSAMPLE),
        ("filename", c_char_p),
    ]
class BASSCHANNEL(object):
 def __init__(self, **kwargs):
  self.__bass = kwargs['bass']
  self._stream = kwargs['stream']
  self.__bass_channelplay=self.__bass._bass.BASS_ChannelPlay
  self.__bass_channelplay.restype=BOOL
  self.__bass_channelplay.argtypes=[HCHANNEL, BOOL]
  self.__bass_channelpause=self.__bass._bass.BASS_ChannelPause
  self.__bass_channelpause.restype=BOOL
  self.__bass_channelpause.argtype=[HCHANNEL]
  self.__bass_channelstop=self.__bass._bass.BASS_ChannelStop
  self.__bass_channelstop.restype=BOOL
  self.__bass_channelstop.argtypes=[HCHANNEL]
  self.__bass_channelgetposition=self.__bass._bass.BASS_ChannelGetPosition
  self.__bass_channelgetposition.restype=QWORD
  self.__bass_channelgetposition.argtypes=[HCHANNEL,DWORD]
  self.__bass_channelsetposition=self.__bass._bass.BASS_ChannelSetPosition
  self.__bass_channelsetposition.restype=BOOL
  self.__bass_channelsetposition.argtypes=[HCHANNEL,QWORD,DWORD]
  self.__bass_channelgetlength=self.__bass._bass.BASS_ChannelGetLength
  self.__bass_channelgetlength.restype=QWORD
  self.__bass_channelgetlength.argtypes=[HCHANNEL,DWORD]
  self.__bass_channelseconds2bytes=self.__bass._bass.BASS_ChannelSeconds2Bytes
  self.__bass_channelseconds2bytes.restype=QWORD
  self.__bass_channelseconds2bytes.argtypes=[HCHANNEL,c_double]
  self.__bass_channelbytes2seconds=self.__bass._bass.BASS_ChannelBytes2Seconds
  self.__bass_channelbytes2seconds.restype=c_double
  self.__bass_channelbytes2seconds.argtypes=[HCHANNEL,QWORD]
  self.__bass_channelflags=self.__bass._bass.BASS_ChannelFlags
  self.__bass_channelflags.restype=DWORD
  self.__bass_channelflags.argtypes=[HCHANNEL,DWORD,DWORD]
  self.__bass_channelget3dattributes=self.__bass._bass.BASS_ChannelGet3DAttributes
  self.__bass_channelget3dattributes.restype=BOOL
  self.__bass_channelget3dattributes.argtypes=[HCHANNEL,POINTER(DWORD),POINTER(c_float),POINTER(c_float),POINTER(DWORD),POINTER(DWORD),POINTER(c_float)]
  self.__bass_channelget3dposition=self.__bass._bass.BASS_ChannelGet3DPosition
  self.__bass_channelget3dposition.restype=BOOL
  self.__bass_channelget3dposition.argtypes=[HCHANNEL,POINTER(bass_vector),POINTER(bass_vector),POINTER(bass_vector)]
  self.__bass_channelgetattribute=self.__bass._bass.BASS_ChannelGetAttribute
  self.__bass_channelgetattribute.restype=BOOL
  self.__bass_channelgetattribute.argtypes=[HCHANNEL,DWORD,POINTER(c_float)]
  self.__bass_channelgetdevice=self.__bass._bass.BASS_ChannelGetDevice
  self.__bass_channelgetdevice.restype=DWORD
  self.__bass_channelgetdevice.argtypes=[HCHANNEL]
  self.__bass_channelsetdevice=self.__bass._bass.BASS_ChannelSetDevice
  self.__bass_channelsetdevice.restype=BOOL
  self.__bass_channelsetdevice.argtypes=[HCHANNEL,DWORD]
  self.__bass_channelgetinfo=self.__bass._bass.BASS_ChannelGetInfo
  self.__bass_channelgetinfo.restype=BOOL
  self.__bass_channelgetinfo.argtypes=[HCHANNEL,POINTER(bass_channelinfo)]
  self.__bass_channelgetlevel=self.__bass._bass.BASS_ChannelGetLevel
  self.__bass_channelgetlevel.restype=DWORD
  self.__bass_channelgetlevel.argtypes=[HCHANNEL]
  self.__bass_channelgettags=self.__bass._bass.BASS_ChannelGetTags
  self.__bass_channelgettags.restype=c_char_p
  self.__bass_channelgettags.argtypes=[HCHANNEL,DWORD]
  self.__bass_channelisactive=self.__bass._bass.BASS_ChannelIsActive
  self.__bass_channelisactive.restype=DWORD
  self.__bass_channelisactive.argtypes=[HCHANNEL]
  self.__bass_channelissliding=self.__bass._bass.BASS_ChannelIsSliding
  self.__bass_channelissliding.restype=BOOL
  self.__bass_channelissliding.argtypes=[HCHANNEL,DWORD]
  self.__bass_channellock=self.__bass._bass.BASS_ChannelLock
  self.__bass_channellock.restype=BOOL
  self.__bass_channellock.argtypes=[HCHANNEL,BOOL]
  self.__bass_channelremovelink=self.__bass._bass.BASS_ChannelRemoveLink
  self.__bass_channelremovelink.restype=BOOL
  self.__bass_channelremovelink.argtypes=[HCHANNEL,DWORD]
  self.__bass_channelset3dattributes=self.__bass._bass.BASS_ChannelSet3DAttributes
  self.__bass_channelset3dattributes.restype=BOOL
  self.__bass_channelset3dattributes.argtypes=[HCHANNEL,c_int,c_float,c_float,c_int,c_int,c_float]
  self.__bass_channelsetattribute=self.__bass._bass.BASS_ChannelSetAttribute
  self.__bass_channelsetattribute.restype=BOOL
  self.__bass_channelsetattribute.argtypes=[HCHANNEL,DWORD,c_float]
  self.__bass_channelset3dposition=self.__bass._bass.BASS_ChannelSet3DPosition
  self.__bass_channelset3dposition.restype=BOOL
  self.__bass_channelset3dposition.argtypes=[HCHANNEL,POINTER(bass_vector),POINTER(bass_vector),POINTER(bass_vector)]
  self.__bass_channelsetfx=self.__bass._bass.BASS_ChannelSetFX
  self.__bass_channelsetfx.restype=HFX
  self.__bass_channelsetfx.argtypes=[HCHANNEL,DWORD,c_int]
  self.__bass_channelsetsync=self.__bass._bass.BASS_ChannelSetSync
  self.__bass_channelsetsync.restype=HSYNC
  self.__bass_channelsetsync.argtypes=[HCHANNEL,DWORD,QWORD,tSyncProc,c_void_p]
  self.__bass_channelgetdata=self.__bass._bass.BASS_ChannelGetData
  self.__bass_channelgetdata.restype=DWORD
  self.__bass_channelgetdata.argtypes=[HCHANNEL,c_void_p,DWORD]
  self.__bass_channelsetdsp=self.__bass._bass.BASS_ChannelSetDSP
  self.__bass_channelsetdsp.restype=HDSP
  self.__bass_channelsetdsp.argtypes=[HCHANNEL,tDspProc,c_void_p]
  self.__bass_channelsetlink=self.__bass._bass.BASS_ChannelSetLink
  self.__bass_channelsetlink.restype=BOOL
  self.__bass_channelsetlink.argtypes=[HCHANNEL,HCHANNEL]
 def Play(self, restart=False):
  result=self.__bass_channelplay(self._stream, restart)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def Pause(self):
  result=self.__bass_channelpause(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def Stop(self):
  result=self.__bass_channelstop(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def GetPosition(self,mode=BASS_POS_BYTE):
  result=self.__bass_channelgetposition(self._stream,mode)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 def SetPosition(self, position,mode):
  result=self.__bass_channelsetposition(self._stream,position,mode)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def GetLength(self,mode):
  result=self.__bass_channelgetlength(self._stream,mode)
  if self.__bass._Error:raise BassExceptionError(self.__bass._Error)
  return int(result)
 def Seconds2Bytes(self,seconds):
  result=self.__bass_channelseconds2bytes(self._stream,seconds)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 def Bytes2Seconds(self,bytes):
  result=self.__bass_channelbytes2seconds(self._stream,bytes)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return result
 def ChannelFlags(self,flags,mask):
  result=self.__bass_channelflags(self._stream,flags,mask)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 def __Get3DAttributes(self):
  mode=DWORD(0)
  min=c_float(0)
  max=c_float(0)
  iangle=DWORD(0)
  oangle=DWORD(0)
  outvol=c_float(0)
  result=self.__bass_channelget3dattributes(self._stream,mode,min,max,iangle,oangle,outvol)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return {'mode':mode.value,'min':min.value,'max':max.value,'iangle':iangle.value,'oangle':oangle.value,'outvol':outvol.value}
 def __Get3DPosition(self):
  pos=bass_vector()
  orient=bass_vector()
  vel=bass_vector()
  result=self.__bass_channelget3dposition(self._stream,pos,orient,vel)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return {'pos':{'X':pos.X,'Y':pos.Y,'Z':pos.Z},'orient':{'X':orient.X,'Y':orient.Y,'Z':orient.Z},'vel':{'X':vel.X,'Y':vel.Y,'Z':vel.Z}}
 def GetAttribute(self, attrib):
  value=c_float(0)
  result=self.__bass_channelgetattribute(self._stream,attrib,value)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return value.value
 @property
 def Device(self):
  result=self.__bass_channelgetdevice(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 @Device.setter
 def Device(self,device):
  result=self.__bass_channelsetdevice(self._stream,device)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
 def __Info(self):
  bret_=bass_channelinfo()
  result=self.__bass_channelgetinfo(self._stream,bret_)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  plugin=(BASSPLUGIN(bass=self.__bass,plugin=bret_.plugin) if bret_.plugin else 0)
  sample=(BASSSAMPLE(bass=self.__bass,stream=bret_.sample) if bret_.sample else 0)
  return {'freq':bret_.freq,'chans':bret_.chans,'flags':bret_.flags,'ctype':bret_.ctype,'origres':bret_.origres,'plugin':plugin,'sample':sample,'filename':bret_.filename}
 @property
 def Frequency(self):
  return int(self.__Info()['freq'])
 @property
 def Channels(self):
  return int(self.__Info()['chans'])
 @property
 def Flags(self):
  return int(self.__Info()['flags'])
 @property
 def Type(self):
  return int(self.__Info()['ctype'])
 @property
 def Resolution(self):
  return int(self.__Info()['origres'])
 @property
 def Plugin(self):
  return self.__Info()['plugin']
 @property
 def Sample(self):
  return self.__Info()['sample']
 @property
 def Filename(self):
  return self.__Info()['filename']
 @property
 def Level(self):
  result=self.__bass_channelgetlevel(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 def GetTags(self,tags):
  result=self.__bass_channelgettags(self._stream,tags)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return result
 @property
 def Active(self):
  result=self.__bass_channelisactive(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(result)
 def IsSliding(self,attrib):
  result=self.__bass_channelissliding(self._stream,attrib)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def Lock(self,lock):
  result=self.__bass_channellock(self._stream,lock)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def __repr__(self):
  return '<BASSCHANNEL object at %s>'%(self._stream)
 def RemoveLink(self, object):
  if not hasattr(object,'_stream'): raise BassParameterError('The object parameter needs to be a valid Bass4Py sub-object')
  result=self.__bass_channelremovelink(self._stream,object._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def __Set3DAttributes(self,mode,min,max,iangle,oangle,outvol):
  result=self.__bass_channelset3dattributes(self._stream,mode,min,max,iangle,oangle,outvol)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def SetAttribute(self,attrib,val):
  result=self.__bass_channelsetattribute(self._stream,attrib,val)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(result)
 def __Set3DPosition(self,pos,orient,vel):
  if type(pos)==types.DictType:
   bpos=bass_vector()
   bpos.X=pos['X']
   bpos.Y=pos['Y']
   bpos.Z=pos['Z']
  else:
   raise BassParameterError('The pos parameter needs to be in dictionary format')
  if type(orient)==types.DictType:
   borient=bass_vector()
   borient.X=orient['X']
   borient.Y=orient['Y']
   borient.Z=orient['Z']
  else:
   raise BassParameterError('The orient parameter needs to be in dictionary format')
  if type(vel)==types.DictType:
   bvel=bass_vector()
   bvel.X=vel['X']
   bvel.Y=vel['Y']
   bvel.Z=vel['Z']
  else:
   raise BassParameterError('The pos parameter needs to be in dictionary format')
  ret_=self.__bass_channelset3dposition(self._stream,bpos,borient,bvel)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)
 @property
 def Position(self):
  return self.__Get3DPosition()['pos']
 @Position.setter
 def Position(self,position):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(position,ret_['orient'],ret_['vel'])
  self.__bass._Apply3D()
 @property
 def Orientation(self):
  return self.__Get3DPosition()['orient']
 @Orientation.setter
 def Orientation(self,orientation):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(ret_['pos'],orientation,ret_['vel'])
  self.__bass._Apply3D()
 @property
 def Velocity(self):
  return self.__Get3DPosition()['vel']
 @Velocity.setter
 def Velocity(self,velocity):
  ret_=self.__Get3DPosition()
  self.__Set3DPosition(ret_['pos'],ret_['orient'],velocity)
  self.__bass._Apply3D()
 @property
 def Mode(self):
  return int(self.__Get3DAttributes()['mode'])
 @Mode.setter
 def Mode(self,mode):
  ret_=self.__Get3DAttributes()
  self.__Set3DAttributes(mode,ret_['min'],ret_['max'],ret_['iangle'],ret_['oangle'],ret_['outvol'])
  self.__bass._Apply3D()
 @property
 def MinDistance(self):
  return self.__Get3DAttributes()['min']
 @MinDistance.setter
 def MinDistance(self,mindistance):
  ret_=self.__Get3DAttributes()
  self.__Set3DAttributes(ret_['mode'],mindistance,ret_['max'],ret_['iangle'],ret_['oangle'],ret_['outvol'])
  self.__bass._Apply3D()
 @property
 def MaxDistance(self):
  return self.__Get3DAttributes()['max']
 @MaxDistance.setter
 def MaxDistance(self,maxdistance):
  ret_=self.__Get3DAttributes()
  self.__Set3DAttributes(ret_['mode'],ret_['min'],maxdistance,ret_['iangle'],ret_['oangle'],ret_['outvol'])
  self.__bass._Apply3D()
 @property
 def Angle(self):
  ret_=self.__Get3DAttributes()
  return {'IAngle':int(ret_['iangle']),'OAngle':int(ret_['oangle'])}
 @Angle.setter
 def Angle(self,angle):
  if type(angle)!=types.DictType: raise BassParameterError('this value must be provided as dictionary')
  ret_=self.__Get3DAttributes()
  self.__Set3DAttributes(ret_['mode'],ret_['min'],ret_['max'],angle['iangle'],angle['oangle'],ret_['outvol'])
  self.__bass._Apply3D()
 @property
 def OutVolume(self):
  return self.__Get3DAttributes()['outvol']
 @OutVolume.setter
 def OutVolume(self,outvolume):
  ret_=self.__Get3DAttributes()
  self.__Set3DAttributes(ret_['mode'],ret_['min'],ret_['max'],ret_['iangle'],ret_['oangle'],outvolume)
  self.__bass._Apply3D()
 def SetFX(self,fx,priority):
  ret_=self.__bass_channelsetfx(self._stream,fx,priority)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  fx=BASSFX(bass=self.__bass,stream=self._stream,fx=fx)
  return fx
 def SetSync(self,synctype,syncparam,syncproc,user=None):
  if type(syncproc)!=types.FunctionType:
   raise BassParameterError('syncproc needs to be a valid function')
  fsyncproc=tSyncProc(syncproc)
  ret_=self.__bass_channelsetsync(self._stream,synctype,syncparam,fsyncproc,user)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  sync=BASSSYNC(bass=self.__bass,stream=self._stream,sync=ret_)
  __callbackreferences__.append(fsyncproc)
  return sync
 def ReceiveSync(self,id):
  return BASSSYNC(bass=self.__bass,stream=self._stream,sync=id)
 def GetData(self,length):
  buffer=(c_short*length)()
  ret_=self.__bass_channelgetdata(self._stream,byref(buffer),length)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return (int(ret_),list(buffer))
 def SetDSP(self,dspproc,user=None):
  if type(dspproc)!=types.FunctionType:
   raise BassParameterError('dspproc needs to be a valid function')
  fdspproc=tDspProc(dspproc)
  ret_=self.__bass_channelsetdsp(self._stream,fdspproc,user)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  dsp=BASSDSP(bass=self.__bass,stream=self._stream,dsp=ret_)
  __callbackreferences__.append(fdspproc)
  return dsp
 def SetLink(self,object):
  if not hasattr(object,'_stream'): raise BassParameterError('The object parameter needs to be a valid Bass4Py sub-object')
  ret_=self.__bass_channelsetlink(self._stream,object._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)