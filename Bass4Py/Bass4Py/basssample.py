from ctypes import *
from .exceptions import *
BOOL=c_long
DWORD=c_ulong
HSAMPLE=DWORD
class bass_sample(Structure):
 _fields_=[("freq",DWORD),("volume",c_float),("pan",c_float),("flags",DWORD),("length",DWORD),("max",DWORD),("origres",DWORD),("chans",DWORD),("mingap",DWORD),("mode3d",DWORD),("mindist",c_float),("maxdist",c_float),("iangle",DWORD),("oangle",DWORD),("outvol",c_float),("vam",DWORD),("priority",DWORD)]
class BASSSAMPLE(object):
 def __init__(self, **kwargs):
  self.__bass=kwargs['bass']
  self._stream=kwargs['stream']
  self.__bass_samplefree=self.__bass._bass.BASS_SampleFree
  self.__bass_samplefree.restype=BOOL
  self.__bass_samplefree.argtypes=[HSAMPLE]
  self.__bass_samplegetchannel=self.__bass._bass.BASS_SampleGetChannel
  self.__bass_samplegetchannel.restype=DWORD
  self.__bass_samplegetchannel.argtypes=[HSAMPLE,BOOL]
  self.__bass_samplegetinfo=self.__bass._bass.BASS_SampleGetInfo
  self.__bass_samplegetinfo.restype=BOOL
  self.__bass_samplegetinfo.argtypes=[HSAMPLE,POINTER(bass_sample)]
  self.__bass_samplegetchannels=self.__bass._bass.BASS_SampleGetChannels
  self.__bass_samplegetchannels.restype=DWORD
  self.__bass_samplegetchannels.argtypes=[HSAMPLE,POINTER(DWORD)]
  self.__bass_samplegetdata=self.__bass._bass.BASS_SampleGetData
  self.__bass_samplegetdata.restype=BOOL
  self.__bass_samplegetdata.argtypes=[HSAMPLE,c_void_p]
  self.__bass_samplesetdata=self.__bass._bass.BASS_SampleSetData
  self.__bass_samplesetdata.restype=BOOL
  self.__bass_samplesetdata.argtypes=[HSAMPLE,c_void_p]
  self.__bass_samplestop=self.__bass._bass.BASS_SampleStop
  self.__bass_samplestop.restype=BOOL
  self.__bass_samplestop.argtypes=[HSAMPLE]
  self.__bass_samplesetinfo=self.__bass._bass.BASS_SampleSetInfo
  self.__bass_samplesetinfo.restype=BOOL
  self.__bass_samplesetinfo.argtypes=[HSAMPLE,POINTER(bass_sample)]
 def __repr__(self):
  return '<BASSSAMPLE object at %d>'%(self._stream)
 def Free(self):
  ret_=self.__bass_samplefree(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)
 def GetChannel(self,onlynew=False):
  ret_=self.__bass_samplegetchannel(self._stream,onlynew)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return self.__bass.ReceiveChannel(ret_)
 def __GetInfo(self):
  bret_=bass_sample()
  ret_=self.__bass_samplegetinfo(self._stream,bret_)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return {"freq":bret_.freq,"volume":bret_.volume,"pan":bret_.pan,"flags":bret_.flags,"length":bret_.length,"max":bret_.max,"origres":bret_.origres,"chans":bret_.chans,"mingap":bret_.mingap,"mode3d":bret_.mode3d,"mindist":bret_.mindist,"maxdist":bret_.maxdist,"iangle":bret_.iangle,"oangle":bret_.oangle,"outvol":bret_.outvol,"vam":bret_.vam,"priority":bret_.priority}
 @property
 def Frequency(self):
  return int(self.__GetInfo()['freq'])
 @Frequency.setter
 def Frequency(self,freq):
  self.__SetInfo(freq=freq)
 @property
 def Volume(self):
  return self.__GetInfo()['volume']
 @Volume.setter
 def Volume(self,vol):
  self.__SetInfo(vol=vol)
 @property
 def Pan(self):
  return self.__GetInfo()['pan']
 @Pan.setter
 def Pan(self,pan):
  self.__SetInfo(pan=pan)
 @property
 def Flags(self):
  return int(self.__GetInfo()['flags'])
 @Flags.setter
 def Flags(self,flags):
  self.__SetInfo(flags=flags)
 @property
 def Length(self):
  return int(self.__GetInfo()['length'])
 @property
 def MaxPlaybacks(self):
  return int(self.__GetInfo()['max'])
 @MaxPlaybacks.setter
 def MaxPlaybacks(self,max):
  self.__SetInfo(max=max)
 @property
 def Resolution(self):
  return int(self.__GetInfo()['origres'])
 @property
 def ChannelCount(self):
  return int(self.__GetInfo()['chans'])
 @property
 def MinGap(self):
  return int(self.__GetInfo()['mingap'])
 @MinGap.setter
 def MinGap(self,mingap):
  self.__SetInfo(mingap=mingap)
 @property
 def Mode3D(self):
  return int(self.__GetInfo()['mode3d'])
 @Mode3D.setter
 def Mode3D(self,mode3d):
  self.__SetInfo(mode3d=mode3d)
 @property
 def MinDistance(self):
  return self.__GetInfo()['mindist']
 @MinDistance.setter
 def MinDistance(self,mindist):
  self.__SetInfo(mindist=mindist)
 @property
 def MaxDistance(self):
  return self.__GetInfo()['maxdist']
 @MaxDistance.setter
 def MaxDistance(self,maxdist):
  self.__SetInfo(maxdist=maxdist)
 @property
 def IAngle(self):
  return int(self.__GetInfo()['iangle'])
 @IAngle.setter
 def IAngle(self,iangle):
  self.__SetInfo(iangle=iangle)
 @property
 def OAngle(self):
  return int(self.__GetInfo()['oangle'])
 @OAngle.setter
 def OAngle(self,oangle):
  self.__SetInfo(oangle=oangle)
 @property
 def OutVolume(self):
  return self.__GetInfo()['outvol']
 @OutVolume.setter
 def OutVolume(self,outvol):
  self.__SetInfo(outvol=outvol)
 @property
 def VAM(self):
  return int(self.__GetInfo()['vam'])
 @VAM.setter
 def VAM(self,vam):
  self.__SetInfo(vam=vam)
 @property
 def Priority(self):
  return int(self.__GetInfo()['priority'])
 @Priority.setter
 def Priority(self,priority):
  self.__SetInfo(priority=priority)
 @property
 def ActiveChannelCount(self):
  count=DWORD(0)
  ret_=self.__bass_samplegetchannels(self._stream,count)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return int(ret_)
 @property
 def Channels(self):
  channels=DWORD*self.ChannelCount
  channels=channels()
  ret_=self.__bass_samplegetchannels(self._stream,channels)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  lchannels=[]
  for channel in channels:
   if channel: lchannels.append(self.__bass.ReceiveChannel(channel))
   else: lchannels.append(0)
  return lchannels
 @property
 def Data(self):
  bdata=(c_short*self.Length)()
  ret_=self.__bass_samplegetdata(self._stream,byref(bdata))
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return list(bdata)
 @Data.setter
 def Data(self,data):
  bdata=(c_short*len(data))()
  for i in range(0,len(data)+1):
   bdata[i]=data[i]
  ret_=self.__bass_samplesetdata(self._stream,byref(bdata))
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
 def Stop(self):
  ret_=self.__bass_samplestop(self._stream)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)
 def __SetInfo(self,**kwargs):
  binfo=bass_sample()
  info=self.__GetInfo()
  for key, value in info.iteritems():
   setattr(binfo,key,value)
  for key, value in kwargs.iteritems():
   setattr(binfo,key,value)
  ret_=self.__bass_samplesetinfo(self._stream,binfo)
  if self.__bass._Error: raise BassExceptionError(self.__bass._Error)
  return bool(ret_)