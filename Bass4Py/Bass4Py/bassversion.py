class BASSVERSION(object):
 def __init__(self, dword):
  self.Dword=int(dword)
  hiword=hex(self.Dword>>16)
  hiword=str(hiword)[2:][:-1].zfill(4)
  loword=hex(self.Dword&0x0000ffff)
  loword=str(loword)[2:][:-1].zfill(4)
  self.Str=''
  verpart=int(hiword[0:2],16)
  if verpart>0: self.Str=str(verpart)+'.'
  verpart=int(hiword[2:],16)
  self.Str=self.Str+str(verpart)+'.'
  verpart=int(loword[0:2],16)
  self.Str=self.Str+str(verpart)
  verpart=int(loword[2:],16)
  if verpart>0:self.Str=self.Str+'.'+str(verpart)
 def __repr__(self):
  return '<BASSVERSION object; representing %d (v%s)>'%(self.Dword,self.Str)