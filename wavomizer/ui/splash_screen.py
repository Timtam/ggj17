import pygame

from ..commons import *
from .controls import *

class SplashScreen:
    def __init__(self, screen):
        self.screen = screen
        self.splash = pygame.transform.scale(get_common().get_image('assets/ui/splash-16by9.png'), self.screen.get_size())
        self.sound = play_sound_fx("assets/sound/ui/splash_screen.ogg")

    def leave(self): pass
    def handle_ev(self, event): pass
    def update(self):
        if self.sound.Active == BASS_ACTIVE_PLAYING and get_common().get_options().get('skip_splash_screen')==False:
            return

        if self.sound.Active==BASS_ACTIVE_PLAYING:
            self.sound.Stop()

        get_common().get_main().change_view('MainMenu')

    def render(self):
        self.screen.blit(self.splash, (0, 0))
