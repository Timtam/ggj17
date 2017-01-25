import os.path
from .constants import SAVE_FILENAME
from .script import Script
import cPickle

# not containing all methods, but instead properties which will be pickled and saved
class DataSafe(object):
    def __init__(self):
        pass

class Options:

    options = {
        'skip_splash_screen': False,
        'vol_bgm': 1.0,
        'vol_fx': 1.0
    }

    def __init__(self):
        self.script= Script()
        self.save_path = os.path.join(self.script.path, SAVE_FILENAME)
        if os.path.isfile(self.save_path):
            with open(self.save_path, 'rb') as f:
                self.__save = cPickle.loads(f.read())
        else:
            self.__save = DataSafe()
        self.init()

    def init(self):
        # this function initializes all options
        # this will be needed if we load an old save file which doesn't contain some new options
        # in this case we will add them with some default value
        # if no save file exists, we'll just add all values brand new

        for key in self.options.keys():
            if not key in self.__save.__dict__:
                self.__save.__dict__[key]=self.options[key]

    def save(self):
        with open(self.save_path, 'wb') as f:
            f.write(cPickle.dumps(self.__save, cPickle.HIGHEST_PROTOCOL))

    def set(self, option, value):
        self.__save.__dict__[option] = value

    def get(self, option):
        return self.__save.__dict__[option]
