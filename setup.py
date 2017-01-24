import shutil
import script
import sys
import os
import os.path
import platform
from cx_Freeze import setup,Executable
def ListAllFiles(path):
 entrylist=os.listdir(path)
 flist=[]
 for entry in entrylist:
  fentry=os.path.join(path,entry)
  if os.path.isdir(fentry):
   nflist=ListAllFiles(fentry)
   flist=flist+nflist
  else:
   flist.append(fentry)
 return flist
def listdlls(folder):
 fileslist=[]
 files=os.listdir(folder)
 for file in files:
  if os.path.isfile(os.path.join(folder,file)):
   ext=os.path.splitext(file)[1]
   if ext.lower()=='.dll':
    fileslist.append(file)
 return fileslist
Script=script.Script()
ScriptDir=Script.Path
build_exe_options={
    "excludes":['email',
        'pygit2',
        'distutils',
        'calendar',
        'numpy',
        'configparser',
        'doctest',
        'ftplib',
        'getpass',
        'optparse',
        'cookielib',
        'win32api',
        'win32con',
        'win32pipe',
        'tarfile',
        'difflib',
        'unittest'
    ]
}

setup(
    name = Script.Name,
    version = Script.Version,
    description = Script.Description,
    options={
        "build_exe":build_exe_options
    },
    executables=[
        Executable(
            "main.py",
            base=(None if platform.system()!="Windows" else "Win32GUI")
        )
    ]
)

BuildDir=os.path.join(ScriptDir, "build", os.listdir(os.path.join(ScriptDir, "build"))[0])

shutil.copytree(os.path.join(ScriptDir,"assets"),os.path.join(BuildDir, "assets"))
bassfile=""
if platform.system()=="Windows":
    bassfile="bass%s.dll"
elif platform.system()=="Linux":
    bassfile = "libbass%s.so"
bassfile=bassfile%("_x64" if sys.maxsize>2**32 else "")
shutil.copyfile(os.path.join(ScriptDir, bassfile), os.path.join(BuildDir, bassfile))

if platform.system()=="Windows":
    import zipfile
    zip=zipfile.ZipFile(os.path.join(ScriptDir,"%s-%s.zip"%(Script.Name,Script.Version)),"w")
    for file in ListAllFiles(BuildDir):
        zip.write(file,'%s-%s\\%s'%(Script.Name,Script.Version,os.path.relpath(file,BuildDir)),zipfile.ZIP_DEFLATED)
    zip.close()
else:
    import tarfile
    tar=tarfile.open('%s-%s.tar.gz'%(Script.Name,Script.Version),'w:gz')
    tar.add(BuildDir,'%s-%s'%(Script.Name,Script.Version))
    tar.close()
shutil.rmtree(BuildDir)
