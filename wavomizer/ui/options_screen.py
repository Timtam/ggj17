import pygame

from ..commons import *
from ..constants import *
from .controls import *

class OptionsScreen:
    def __init__(self, screen):
        self.bgm = play_sound_bgm('assets/sound/bgm/options.ogg')
        self.screen = screen
        self.controls = []
        panel = PanelControl((self.screen.get_width() - 350) / 2, 200, 350, 350)
        self.controls.append(panel)
        panel.add_child_control(TextControl(20, 20, 'Music'))
        options = get_common().get_options();
        self.bgm_slider = SliderControl(20, 50, 310, None, options.get('vol_bgm'))
        panel.add_child_control(self.bgm_slider)
        panel.add_child_control(TextControl(20, 100, 'Sound effects'))
        self.fx_slider = SliderControl(20, 130, 310, self.fx_slider_release, options.get('vol_fx'))
        panel.add_child_control(self.fx_slider)
        self.splash_checkbox = CheckboxControl(20, 180)
        if options.get('skip_splash_screen'):
            self.splash_checkbox.set_state(CHECKBOX_CHECKED)
        panel.add_child_control(self.splash_checkbox)
        panel.add_child_control(TextControl(60, 185, 'Skip splash screen'))
        panel.add_child_control(ButtonControl(20, 300, 'Cancel', self.cancel_clicked, 150))
        panel.add_child_control(ButtonControl(180, 300, 'Save', self.save_clicked, 150))

    def leave(self):
        self.bgm.Stop()

    def cancel_clicked(self):
        get_common().get_main().change_view('MainMenu')
    def save_clicked(self):
        options = get_common().get_options()
        options.set('vol_fx', self.fx_slider.slider_pos)
        options.set('vol_bgm', self.bgm_slider.slider_pos)
        if self.splash_checkbox.get_state() == CHECKBOX_CHECKED:
            options.set('skip_splash_screen', True)
        else:
            options.set('skip_splash_screen', False)
        options.save()
        get_common().get_main().change_view('MainMenu')

    def fx_slider_release(self):
        play_sound_fx('assets/sound/ui/click.ogg', self.fx_slider.slider_pos)

    def handle_ev(self, event):
        pass

    def update(self):
        for control in self.controls:
            control.update()
        self.bgm.SetAttribute(BASS_ATTRIB_VOL, self.bgm_slider.slider_pos)

    def render(self):
        for control in self.controls:
            control.draw(self.screen)
