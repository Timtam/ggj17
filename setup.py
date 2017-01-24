# This is the distutils script for creating a Python-based com (exe or dll)
# server using win32com.  This script should be run like this:
#
#  % python setup.py py2exe
#
# After you run this (from this directory) you will find two directories here:
# 'build' and 'dist'.  The .dll or .exe in dist is what you are looking for.
##############################################################################
import shutil
from wavomizer import script
import sys
import os
import os.path
import py2exe
def is_system_dll(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ('libfreetype-6.dll', 'libogg-0.dll', 'sdl_ttf.dll'): # 'sdl_ttf.dll' added by arit.
        return 0
    return orig_is_system_dll(pathname) # return the orginal function

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

def list_dlls(folder):
    fileslist = []
    files = os.listdir(folder)
    for file in files:
        if os.path.isfile(os.path.join(folder, file)):
            ext = os.path.splitext(file)[1]
            if ext.lower() == '.dll':
                fileslist.append(file)
    return fileslist

orig_is_system_dll = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
py2exe.build_exe.isSystemDLL = is_system_dll # override the default function with this one

script = script.Script()
script_dir = script.path
os.chdir(script_dir)

from distutils.core import setup
import py2exe
import zipfile
if len(sys.argv) == 1: sys.argv.append('py2exe')
build_dir = script_dir + '/build'
dist_dir = script_dir + '/dist'
py2exe_options = {
    'ascii': False,
    'excludes': ['email',
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
        'unittest'],
    'dll_excludes': ['w9xpopen.exe'],
    'bundle_files': 3,
    'optimize': 2,
    'compressed': True}
setupparameters = {
    'name': script.name,
    'options': {'py2exe': py2exe_options},
    'zipfile': None,
    'version': script.version,
    'description': script.description,
    'author': script.author,
    'author_email': script.email,
    'windows': [{'script': 'wavomizer.py', 'other_resources': script.resources()}]}
setup(**setupparameters)
zip = zipfile.ZipFile(os.path.join(script_dir, '{0}-{1}.zip'.format(script.name, script.version)), 'w')
for file in list_all_files(dist_dir):
    zip.write(file, '{0}-{1}/{2}'.format(script.name, script.version, os.path.relpath(file, dist_dir)), zipfile.ZIP_DEFLATED)
for file in list_dlls(script_dir):
    zip.write(os.path.join(script_dir, file), '{0}-{1}/{2}'.format(script.name, script.version, file), zipfile.ZIP_DEFLATED)
for file in list_all_files(os.path.join(script_dir, 'assets')):
    zip.write(file, '{0}-{1}/assets/{2}'.format(script.name, script.version, os.path.relpath(file, os.path.join(script_dir, 'assets'))), zipfile.ZIP_DEFLATED)
zip.close()
shutil.rmtree(build_dir)
shutil.rmtree(dist_dir)
