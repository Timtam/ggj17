import shutil
from wavomizer import script
import sys
import os
import os.path
import platform
from cx_Freeze import setup,Executable

def list_all_files(path):
    entrylist = os.listdir(path)
    flist = []
    for entry in entrylist:
        fentry = os.path.join(path, entry)
        if os.path.isdir(fentry):
            nflist = list_all_files(fentry)
            flist = flist + nflist
        else:
            flist.append(fentry)
    return flist

script = script.Script()

build_exe_options = {
    "excludes":
    [
        'email',
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
    name = script.name,
    version = script.version,
    description = script.description,
    options = {
        'build_exe' : build_exe_options
    },
    executables = [
        Executable(
            'wavomizer.py',
            base=(None if platform.system() != 'Windows' else 'Win32GUI')
        )
    ]
)

build_dir = os.path.join(script.path, 'build', os.listdir(os.path.join(script.path, 'build'))[0])

shutil.copytree(os.path.join(script.path, 'assets'), os.path.join(build_dir, 'assets'))
bass_file=''
if platform.system()=='Windows':
    bass_file='bass%s.dll'
elif platform.system()=='Linux':
    bass_file = 'libbass%s.so'
bass_file=bass_file%('_x64' if sys.maxsize > 2**32 else '')
shutil.copyfile(os.path.join(script.path, bass_file), os.path.join(build_dir, bass_file))

if platform.system()=='Windows':
    import zipfile
    zip=zipfile.ZipFile(os.path.join(script.path, '%s-%s.zip'%(script.name, script.version)), "w")
    for file in list_all_files(build_dir):
        zip.write(file,'%s-%s\\%s'%(script.name, script.version, os.path.relpath(file,build_dir)), zipfile.ZIP_DEFLATED)
    zip.close()
else:
    import tarfile
    tar=tarfile.open('%s-%s.tar.gz'%(script.name, script.version),'w:gz')
    tar.add(build_dir, '%s-%s'%(script.name, script.version))
    tar.close()
shutil.rmtree(os.path.join(script.path, "build"))
