import pygame

from commons import *
from controls import *

class MainMenu:
    def __init__(self, screen):
        self.channel = play_sound_bgm('assets/sound/bgm/ui.ogg')
        self.screen = screen
        self.controls = []
        self.controls.append(ButtonControl((self.screen.get_width() - 190) / 2, 300, 'New game', self.new_game_clicked))
        self.controls.append(ButtonControl((self.screen.get_width() - 190) / 2, 350, 'Options', self.options_clicked))
        self.controls.append(ButtonControl((self.screen.get_width() - 190) / 2, 400, 'Exit', self.exit_clicked))
        self.controls.append(ButtonControl((self.screen.get_width() - 190) / 2, 450, 'Credits', self.credits_clicked))

    def leave(self):
        self.channel.Stop()

    def new_game_clicked(self):
        get_common().get_main().change_view('Level')

    def options_clicked(self):
        get_common().get_main().change_view('OptionsScreen')

    def exit_clicked(self):
        get_common().get_main().stop()

    def credits_clicked(self):
        get_common().get_main().change_view('Credits')

    def handle_ev(self, event):
        pass

    def update(self):
        for control in self.controls:
            control.update()

    def render(self):
        for control in self.controls:
            control.draw(self.screen)
