from commons import *

def play_sound_fx(filename, volume = None):
	common = get_common()
	channel = common.get_sound(filename)
	if volume == None:
		volume = common.get_options().vol_fx
	channel.SetAttribute(BASS_ATTRIB_VOL, volume)
	channel.Play()
	return channel

def play_sound_bgm(filename, volume = None):
	common = get_common()
	channel = common.get_sound(filename, True)
	if volume == None:
		volume = common.get_options().vol_bgm
	channel.SetAttribute(BASS_ATTRIB_VOL, volume)
	channel.Play(True)
	return channel
