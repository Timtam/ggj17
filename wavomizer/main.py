import sys, time, pygame

from .commons   import *
from .engine.level     import Level
from .ui.main_menu import MainMenu
from .ui.options_screen import OptionsScreen
from .ui.splash_screen import SplashScreen
from .ui.credits_screen import CreditsScreen

class Main:
    def __init__(self, width = 1280, height = 720):
        get_common().load(self)
        self.width  = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.views = {
            'SplashScreen': SplashScreen,
            'MainMenu': MainMenu,
            'OptionsScreen': OptionsScreen,
            'Level': Level,
            'Credits': CreditsScreen,
        }
        self.next_view = None
        self.current_view = None
        self.change_view('MainMenu')
        pygame.display.set_caption('Wavomizer')

    def button_clicked(self):
        pass

    def main_loop(self):
        while True:
            if self.next_view != None:
                if self.current_view != None:
                    self.current_view.leave()
                self.current_view = self.next_view
                self.next_view = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                self.handle_ev(event)
            self.update()
            self.render()
            time.sleep(0.01)

    def stop(self):
        pygame.quit()
        sys.exit()

    def change_view(self, view):
        self.next_view = self.views[view](self.screen)

    def handle_ev(self, event):
        self.current_view.handle_ev(event)

    def update(self):
        self.current_view.update()

    def render(self):
        self.screen.fill((0,0,0))
        self.current_view.render()
        pygame.display.flip()
