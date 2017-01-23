import pygame

from commons import *
from controls import *

class Credits:
    def __init__(self, screen):
        self.screen = screen
        self.bgm = play_sound_bgm('assets/sound/bgm/credits.ogg')
        self.controls = []
        self.controls.append(ButtonControl(20, 20, 'Back to Menu', self.back_to_menu_clicked))
        self.render_surface()

    def back_to_menu_clicked(self):
        get_common().get_main().change_view('MainMenu')

    def render_surface(self):
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        font = get_common().get_font_small()

        label = font.render('---CREDITS---', 1, (255, 255, 255))
        self.surface.blit(label, ((self.surface.get_width() / 2 - 50), self.surface.get_height() * 0.06))

        #BALANCE-BEGIN
        label = font.render('---GAME PERFORMANCE---', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.111, self.surface.get_height() * 0.15))

        label = font.render('Luise Rixrath', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.154, self.surface.get_height() * 0.2))

        label = font.render('Henry Radke', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.155, self.surface.get_height() * 0.25))

        label = font.render('Moritz Bloch', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.154, self.surface.get_height() * 0.3))

        #SOUND-BEGIN
        label = font.render('---SOUND---', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.151, self.surface.get_height() * 0.45))

        label = font.render('Toni Barth', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.156, self.surface.get_height() * 0.55))

        label = font.render('Max Haarbach', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.149, self.surface.get_height() * 0.5))
        #SOUND-END


        #PROGRAMMER-BEGIN
        label = font.render('---PROGRAMMER---', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.73, self.surface.get_height() * 0.15))

        label = font.render('Erik Tauchert', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.75, self.surface.get_height() * 0.2))

        label = font.render('Christian Arp', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.7528, self.surface.get_height() * 0.25))

        label = font.render('Toni Barth', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.761, self.surface.get_height() * 0.3))

        label = font.render('Moritz Bloch', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.753, self.surface.get_height() * 0.35))
        #PROGRAMMER-END

        #ART-BEGIN
        label = font.render('---ART---', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.7585, self.surface.get_height() * 0.45))

        label = font.render('David Siering', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.7525, self.surface.get_height() * 0.5))

        label = font.render('Henry Radke', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.7531, self.surface.get_height() * 0.55))
        #ART-ENDE

        #Licenses-Begin
        label = font.render('---LICENSES---', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.453, self.surface.get_height() * 0.65))


        label = font.render('Kevin McLeod: http://www.incompetech.com', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.366, self.surface.get_height() * 0.7))

        label = font.render('TeknoAXE: http://teknoaxe.com/Home.php', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.369, self.surface.get_height() * 0.75))

        label = font.render('bass (free for non-commercial use)', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.387, self.surface.get_height() * 0.8))

        label = font.render('Kenney Game Assets (CC0)', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.424, self.surface.get_height() * 0.85))

        label = font.render('py2exe (MIT),  Pygame (LGPL v3),  Python (PSF)', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.365, self.surface.get_height() * 0.9))

        label = font.render('Hochschule Anhalt', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.115, self.surface.get_height() * 0.955))

        label = font.render('Prof. Dr. Schlechtweg-Dorendorf', 1, (255, 255, 255))
        self.surface.blit(label, (self.surface.get_width() * 0.734, self.surface.get_height() * 0.955))


        #Licenses-END

        #pics-Begin
        self.surface.blit(pygame.transform.scale(get_common().get_image('assets/level/enemies/skeleton_left.png'), (200, 200)), (self.surface.get_width() * 0.75, self.surface.get_height() * 0.65))

        self.surface.blit(pygame.transform.scale(get_common().get_image('assets/level/towers/watertower.png'), (120, 220)), (self.surface.get_width() * 0.13, self.surface.get_height() * 0.65))

        self.surface.blit(pygame.transform.scale(get_common().get_image('assets/credits/ggj_pix.png'), (450, 250)), (self.surface.get_width() * 0.335, self.surface.get_height() * 0.199))

        #pics-end

    def render(self):
        self.screen.blit(self.surface, (0, 0))
        for control in self.controls:
            control.draw(self.screen)

    def update(self):
        for control in self.controls:
            control.update()

    def leave(self):
        self.bgm.Stop()

    def handle_ev(self, event):
        pass
