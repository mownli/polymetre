#!/usr/bin/env python3
from random import randrange
from typing import List

from polymetre.audio_data import AudioData
from polymetre.audio_player import AudioPlayer
from polymetre.ui import TkUI


class Sentry:

	def __init__(self, data: AudioData, player: AudioPlayer, ui: TkUI):
		self.data = data
		self.player = player
		self.ui = ui

		self.ui.set_metre_button_cb(self.metre_button_cb)
		self.ui.set_start_button_cb(self.start_button_cb)
		self.ui.set_bpm_spinbox_cb(self.bpm_spinbox_cb)
		self.ui.set_silencer_checkbox_cb(self.silencer_checkbox_cb)

		self.current_intervals = [row.head for row in self.data.intervals]
		self.playing = False
		self.silencer_on = False
		self.timeout = 50

	def update_pos(self, blocking=True) -> bool:
		got, frame_pos = self.player.get_head(blocking)
		if not got:
			return False

		for i_metre, node in enumerate(self.current_intervals):
			for i_beat in range(len(self.data.intervals[i_metre])):  # Guard for infinite loop
				begin, end = node.data
				if begin <= frame_pos < end:
					self.current_intervals[i_metre] = node
					break
				node = node.next
		return True

	def get_current_beat_list(self) -> List[int]:
		ret: List[int] = [self.data.intervals[i].index(row) for i, row in enumerate(self.current_intervals)]
		return ret

	def draw_timer(self):
		if self.playing:
			if self.update_pos(blocking=False):
				self.ui.set_current_beat(self.get_current_beat_list())
			self.ui.window.after(self.timeout, self.draw_timer)

	def start_or_stop(self):
		if not self.playing:
			# if not self.ui.check_input():
			# 	return
			if self.silencer_on:
				self.ui.window.after(randrange(1000, 10000), self.silencer_timer)
			self.player.muted = False
			self.player.start()
			self.ui.start_button.config(text='Stop')
			self.playing = True
			self.draw_timer()
		else:
			self.player.stop()
			self.ui.start_button.config(text='Start')
			self.playing = False

	def start_button_cb(self):
		self.start_or_stop()

	def metre_button_cb(self):
		metre_list = self.ui.get_metre()
		if metre_list is None:
			return

		bpm = self.ui.get_bpm()
		if bpm is None:
			return

		self.player.abort()
		self.ui.start_button.config(text='Start')
		self.playing = False
		self.reload_data(metre_list, bpm)
		self.ui.load_beat_display(metre_list)

	def bpm_spinbox_cb(self):
		bpm = self.ui.get_bpm()
		if bpm is not None:
			self.reload_data(self.data.metre_list, bpm)

	def silencer_timer(self):
		if not self.playing:
			self.player.muted = False
			return

		if self.silencer_on:
			self.player.muted = not self.player.muted
			self.ui.window.after(randrange(1000, 10000), self.silencer_timer)
		else:
			self.player.muted = False

	def silencer_checkbox_cb(self):
		self.silencer_on = self.ui.silencer_var.get()
		self.silencer_timer()

		print(self.player.muted)

	def reload_data(self, metre_list: List[int], bpm: int):
		_, pos = self.player.get_head()
		pos_to_frame_ratio = pos / len(self.data.frame)

		self.data.reload(self.data.sample_rate, metre_list, bpm, self.data.bit_depth)
		self.current_intervals = [row.head for row in self.data.intervals]

		self.player.set_data(self.data.frame)
		self.player.set_head(int(len(self.data.frame) * pos_to_frame_ratio))


def main():
	metre = [3, 4]
	bpm = 60

	ui = TkUI(metre, bpm)
	ad = AudioData(metre, bpm)
	ap = AudioPlayer(ad.frame, ad.channel_n, ad.sample_rate, ad.bit_depth)
	sentry = Sentry(ad, ap, ui)

	ui.mainloop()


# np.save('1.npy', rr)
if __name__ == "__main__":
	main()
