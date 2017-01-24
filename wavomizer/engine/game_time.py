import time as org_time

class GameTime:
    instance = None

    def __init__(self):
        self.total_time = 0.0
        self.elapsed_time = 0.0
        self.time_scale = 1.0
        self.last_frame = org_time.time()
        self.paused = False
        GameTime.instance = self

    def time(self):
        return self.total_time
    def frame_time(self):
        return self.elapsed_time
    def set_time_scale(self, time_scale):
        self.time_scale = time_scale
    def pause_time(self):
        self.paused = True
    def resume_time(self):
        self.paused = False

    def start_frame(self):
        current_time = org_time.time()
        time_delta = current_time - self.last_frame
        if not self.paused:
            self.total_time += time_delta * self.time_scale
        self.elapsed_time = time_delta * self.time_scale
        self.last_frame = current_time

def get_game_time_instance():
    if GameTime.instance == None:
        GameTime()
    return GameTime.instance
def time():
    return get_game_time_instance().time()
def frame_time():
    return get_game_time_instance().frame_time()
def set_time_scale(time_scale):
    get_game_time_instance().set_time_scale(time_scale)
def start_frame():
    get_game_time_instance().start_frame()
def pause_time():
    get_game_time_instance().pause_time()
def resume_time():
    get_game_time_instance().resume_time()
