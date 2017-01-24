import os.path
import time
import sys
# loads of unused stuff in here
# usually I link in win32api and pygit2
# to retrieve some relevant data
# since we don't need those dependencies
# just remove them and set those two to False
git_loaded = False
win32_api_loaded = False
class Script:
    def __init__(self):
        self.__stable = 'Stable'
        self.__development = 'Development'
        self.version = '1.0'
        self.company = 'Global Game Jam 2017'
        self.author = 'Team Ultra Lauch'
        self.email = 'toni.barth@student.hs-anhalt.de'
        self.website = 'http://www.globalgamejam.org/'
        self.name = 'Wavomizer'
        self.description = 'Wave your way into freedom! Defend your base against waves of enemies, using your own special way of waves, all together designed to protect you and everything you\'ve got. And not to forget, wave as much as you can...'
        self.copyright = 'Copyright 2017 by Hochschule Anhalt'
    def __path(self):
        if hasattr(sys, 'frozen') and sys.frozen in ['console_exe', 'windows_exe']:
            path = unicode(os.path.dirname(sys.executable))
        else:
            path = os.path.dirname(unicode(os.path.abspath(sys.argv[0])))
        bdir = os.path.isdir(path)
        while not bdir:
            path = os.path.abspath(path + '/..')
            bdir = os.path.isdir(path)
        return path
    def __executable(self):
        if hasattr(sys, 'frozen') and sys.frozen in ['console_exe', 'windows_exe']:
            return True
        else:
            return False
    def __revision_number(self):
        if self.executable and win32_api_loaded:
            return LoadResource(0, u'REVISIONNUMBER', 1)
        elif git_loaded:
            try:
                repo = pygit2.Repository(os.path.join(self.path, '.git'))
            except KeyError:
                return '0'
            revcount = 0
            for commit in repo.lookup_reference(repo.head.name).log():
                revcount += 1
            return str(revcount)
        else:
            return '0'
    def __build_date(self):
        if self.executable and win32_api_loaded:
            return LoadResource(0, u'BUILDDATE', 1)
        elif git_loaded:
            try:
                repo = pygit2.Repository(os.path.join(self.path, '.git'))
            except KeyError:
                return '00-00-00 00:00:00'
            headrev = repo.get(repo.head.target)
            ltime = time.localtime(headrev.commit_time)
            return str(ltime.tm_year) + '-' + str(ltime.tm_mon) + '-' + str(ltime.tm_mday) + ' ' + str(ltime.tm_hour) + ':' + str(ltime.tm_min) + ':' + str(ltime.tm_sec)
        else:
            return '00-00-00 00:00:00'
    def __release_notes(self):
        if self.executable and win32_api_loaded:
            return LoadResource(0, u'RELEASENOTES', 1)
        elif git_loaded:
            try:
                repo = pygit2.Repository(os.path.join(self.path, '.git'))
            except KeyError:
                return '---'
            if self.version_tag == self.__stable:
                taglist = []
                commit = repo.get(repo.head.target)
                for ref in repo.listall_references():
                    oref = repo.revparse_single(ref)
                    if oref.type == pygit2.GIT_OBJ_TAG and oref.hex == commit.hex:
                        return oref.message
                return commit.message
            else:
                commit = repo.get(repo.head.target)
                return commit.message
        else:
            return '---'
    def __version_tag(self):
        if self.executable and win32_api_loaded:
            return LoadResource(0, u'VERSIONTAG', 1)
        elif git_loaded:
            tag = self.__development
            try:
                repo = pygit2.Repository(os.path.join(self.path, '.git'))
            except KeyError:
                return 'Unknown'
            taglist = []
            for ref in repo.listall_references():
                if ref.find('tags') >= 0:
                    oref = repo.revparse_single(ref)
                    taglist.append(oref.hex)
            if len(taglist) > 0:
                if repo.get(repo.head.target).hex in taglist:
                    tag = self.__stable
            return tag
        else:
            return 'Unknown'
    def __version_hash(self):
        if self.executable and win32_api_loaded:
            return LoadResource(0,u'VERSIONHASH',1)
        elif git_loaded:
            try:
                repo = pygit2.Repository(os.path.join(self.path, '.git'))
            except KeyError:
                return '0000000000000000000000000000000000000000'
            return repo.get(repo.head.target).hex
        else:
            return '0000000000000000000000000000000000000000'
    def resources(self):
        resources = []
        resources.append((u'REVISIONNUMBER', 1, self.revision_number))
        resources.append((u'BUILDDATE', 1, self.build_date))
        resources.append((u'VERSIONTAG', 1, self.version_tag))
        resources.append((u'RELEASENOTES', 1, self.release_notes))
        resources.append((u'VERSIONHASH', 1, self.version_hash))
        return resources
    path = property(__path)
    executable = property(__executable)
    revision_number = property(__revision_number)
    version_tag = property(__version_tag)
    build_date = property(__build_date)
    release_notes = property(__release_notes)
    version_hash = property(__version_hash)
