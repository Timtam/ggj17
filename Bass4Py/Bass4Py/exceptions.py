from .constants import *
_ErrorExceptionIndex_ ={BASS_ERROR_MEM:'memory error',
                        BASS_ERROR_FILEOPEN:'can\'t open the file',
                        BASS_ERROR_DRIVER:'can\'t find a free/valid driver',
                        BASS_ERROR_BUFLOST:'the sample buffer was lost',
                        BASS_ERROR_HANDLE:'invalid handle',
                        BASS_ERROR_FORMAT:'unsupported sample format',
                        BASS_ERROR_POSITION:'invalid position',
                        BASS_ERROR_INIT:'BASS.Init has not been successfully called',
                        BASS_ERROR_START:'BASS.Start has not been successfully called',
                        BASS_ERROR_SSL:'https support not available',
                        BASS_ERROR_ALREADY:'already initialized/paused/whatever',
                        BASS_ERROR_NOCHAN:'can\'t get a free channel',
                        BASS_ERROR_ILLTYPE:'an illegal type was specified',
                        BASS_ERROR_ILLPARAM:'an illegal parameter was specified',
                        BASS_ERROR_NO3D:'no 3D support',
                        BASS_ERROR_NOEAX:'no EAX support',
                        BASS_ERROR_DEVICE:'illegal device number',
                        BASS_ERROR_NOPLAY:'not playing',
                        BASS_ERROR_FREQ:'illegal sample rate',
                        BASS_ERROR_NOTFILE:'the stream is not a file stream',
                        BASS_ERROR_NOHW:'no hardware voices available',
                        BASS_ERROR_EMPTY:'the MOD music has no sequence data',
                        BASS_ERROR_NONET:'no internet connection could be opened',
                        BASS_ERROR_CREATE:'couldn\'t create the file',
                        BASS_ERROR_NOFX:'effects are not available',
                        BASS_ERROR_NOTAVAIL:'requested data is not available',
                        BASS_ERROR_DECODE:'the channel is a "decoding channel',
                        BASS_ERROR_DX:'a sufficient DirectX version is not installed',
                        BASS_ERROR_TIMEOUT:'connection timedout',
                        BASS_ERROR_FILEFORM:'unsupported file format',
                        BASS_ERROR_SPEAKER:'unavailable speaker',
                        BASS_ERROR_VERSION:'invalid BASS version (used by add-ons)',
                        BASS_ERROR_CODEC:'codec is not available/supported',
                        BASS_ERROR_ENDED:'the channel/file has ended',
                        BASS_ERROR_BUSY:'the device is busy',
                        BASS_ERROR_UNKNOWN:'some mystery problem'}

class BassLibError(Exception):
 pass
class BassExceptionError(Exception):
 def __init__(self, errorcode):
  self.code=errorcode
 def __str__(self):
  return 'BassError: \n\tErrorcode: %d\n\tErrormessage: %s'%(self.code,_ErrorExceptionIndex_[self.code] if self.code in _ErrorExceptionIndex_ else 'Not available')
 message=property(__str__)
class BassParameterError(Exception):
 pass
class BassDWORDError(Exception):
 def __str__(self):
  return 'BASS returned a value which indicates an error. This value might not be available in BASS\' current state.'
 message=property(__str__)
class BassEAXError(Exception):
 def __str__(self):
  return 'Unable to perform this operation: EAX is not available on your system'
 message=property(__str__)