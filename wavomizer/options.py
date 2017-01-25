import os.path
from .script import Script

class Options:
    def __init__(self):
        self.vol_fx = 1
        self.vol_bgm = 1
        self.script= Script()
        if os.path.isfile(os.path.join(self.script.path, 'options.txt')):
            with open(os.path.join(self.script.path, 'options.txt'), 'r') as f:
                for line in f:
                    if line.startswith('vol_fx='):
                        self.vol_fx = float(line[7:])
                    elif line.startswith('vol_bgm='):
                        self.vol_bgm = float(line[8:])
    def save(self):
        with open(os.path.join(self.script.path, 'options.txt'), 'w') as f:
            f.write('vol_fx=' + str(self.vol_fx) + '\n')
            f.write('vol_bgm=' + str(self.vol_bgm) + '\n')
