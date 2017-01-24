import os.path

class Options:
    def __init__(self):
        self.vol_fx = 1
        self.vol_bgm = 1
        if os.path.isfile('options.txt'):
            with open('options.txt', 'r') as f:
                for line in f:
                    if line.startswith('vol_fx='):
                        self.vol_fx = float(line[7:])
                    elif line.startswith('vol_bgm='):
                        self.vol_bgm = float(line[8:])
    def save(self):
        with open('options.txt', 'w') as f:
            f.write('vol_fx=' + str(self.vol_fx) + '\n')
            f.write('vol_bgm=' + str(self.vol_bgm) + '\n')
