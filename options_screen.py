import pygame

from commons import *
from controls import *

class OptionsScreen:
	def __init__(self, screen):
		self.screen = screen
		self.controls = []
		panel = PanelControl((self.screen.get_width() - 350) / 2, 200, 350, 350)
		self.controls.append(panel)
		panel.add_child_control(TextControl(20, 20, 'Musik'))
		options = get_common().get_options();
		self.bgm_slider = SliderControl(20, 50, 310, self.bgm_slider_release, options.vol_bgm)
		panel.add_child_control(self.bgm_slider)
		panel.add_child_control(TextControl(20, 100, 'Effekte'))
		self.fx_slider = SliderControl(20, 130, 310, self.fx_slider_release, options.vol_fx)
		panel.add_child_control(self.fx_slider)
		panel.add_child_control(ButtonControl(20, 300, 'Abbrechen', self.cancel_clicked, 150))
		panel.add_child_control(ButtonControl(180, 300, 'Speichern', self.save_clicked, 150))

	def leave(self):
		pass

	def cancel_clicked(self):
		get_common().get_main().change_view('MainMenu')
	def save_clicked(self):
		options = get_common().get_options()
		options.vol_fx = self.fx_slider.slider_pos
		options.vol_bgm = self.bgm_slider.slider_pos
		get_common().get_main().change_view('MainMenu')

	def bgm_slider_release(self): pass
	def fx_slider_release(self):
		play_sound_fx('assets/sound/ui/switch26.ogg', self.fx_slider.slider_pos)


	def handle_ev(self, event):
		pass

	def update(self):
		for control in self.controls:
			control.update()

	def render(self):
		for control in self.controls:
			control.draw(self.screen)
