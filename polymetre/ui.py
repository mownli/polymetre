import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from typing import List

from polymetre.utils import find_lcm


class TkUI:

	title = 'Polymetre'

	def __init__(self, metre_list: List[int], bpm: int):
		self.window = tk.Tk()
		self.window.title(self.title)
		self.window.columnconfigure(0, weight=1)
		self.window.rowconfigure(1, weight=1)

		self.settings_frame = ttk.Frame(self.window)
		self.settings_frame.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W, padx=5, pady=5)
		self.settings_frame.columnconfigure(0, weight=1)
		self.settings_frame.columnconfigure(1, weight=1)
		self.settings_frame.columnconfigure(2, weight=1)

		self.metre_label = ttk.Label(self.settings_frame, text='Metre:', anchor='e')
		self.metre_label.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

		self.metre_string = tk.StringVar()
		self.metre_entry = ttk.Entry(self.settings_frame, textvariable=self.metre_string)
		self.metre_entry.grid(column=1, row=0, sticky=tk.N + tk.E + tk.S + tk.W, padx=5)

		self.metre_button = ttk.Button(self.settings_frame, text='Apply')
		self.metre_button.grid(column=2, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

		self.bpm_label = ttk.Label(self.settings_frame, text='BPM:', anchor='e')
		self.bpm_label.grid(column=0, row=1, sticky=tk.N+tk.E+tk.S+tk.W)

		self.bpm_var = tk.StringVar()
		self.bpm_spinbox = ttk.Spinbox(self.settings_frame, from_=1, to=999, textvariable=self.bpm_var)
		self.bpm_spinbox.grid(column=1, row=1, sticky=tk.N+tk.E+tk.S+tk.W, padx=5)

		self.start_button = ttk.Button(self.settings_frame, text='Start')
		self.start_button.grid(column=2, row=1, sticky=tk.N+tk.E+tk.S+tk.W)

		self.silencer_var = tk.IntVar()
		self.silencer_checkbutton = ttk.Checkbutton(
			self.settings_frame,
			text='Random silences',
			variable=self.silencer_var,
			onvalue=1,
			offvalue=0,
			command=self.set_start_button_cb)
		self.silencer_checkbutton.grid(column=0, row=2, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=3)

		self.beat_display = []
		self.current_beat_labels: List[tk.Label] = []
		self.beat_frame = ttk.Frame(self.window)
		self.beat_frame.grid(column=0, row=1, sticky=tk.N+tk.E+tk.S+tk.W, pady=5, padx=5)

		self.metre_string.set(', '.join([str(i) for i in metre_list]))
		self.bpm_var.set(bpm)
		self.load_beat_display(metre_list)

		self.start_button.focus_set()

	def set_start_button_cb(self, callback):
		self.start_button.config(command=callback)

	def set_metre_button_cb(self, callback):
		def cb():
			callback()

		self.metre_button.config(command=cb)

	def set_bpm_spinbox_cb(self, callback):
		def cb(_, __, ___):
			callback()

		self.bpm_var.trace('w', cb)

	def set_silencer_checkbox_cb(self, callback):
		self.silencer_checkbutton.config(command=callback)

	def get_bpm(self):
		try:
			ret = int(self.bpm_var.get())
			if 0 < ret <= 999:
				return ret
		except ValueError:
			mb.showerror(title='Error', message='Bad input')
			return None

	def check_input(self) -> bool:
		m = self.get_metre()
		if m is None:
			return False
		b = self.get_bpm()
		if b is None:
			return False
		return True

	def get_metre(self):
		try:
			meter_list = [int(s) for s in self.metre_string.get().split(',')]
		except ValueError:
			mb.showerror(title='Error', message='Bad input')
			return None

		for i in meter_list:
			if i <= 0:
				mb.showerror(title='Error', message='Bad input')
				return None
		return meter_list

	def load_beat_display(self, beats: List[int]):
		self._beat_frame_clear()
		self.current_beat_labels.clear()

		column_n = find_lcm(beats)
		for i in range(column_n):
			self.beat_frame.columnconfigure(i, weight=1)

		for i in range(len(beats)):
			self.beat_frame.rowconfigure(i, weight=1)

		for i_beat, beat in enumerate(beats):
			self.beat_display.append([])
			beat_column_len = int(column_n / beat)
			for i in range(beat):
				self.beat_display[-1].append(tk.Label(self.beat_frame, bg='black'))
				self.beat_display[-1][-1].grid(
					column=i*beat_column_len,
					columnspan=beat_column_len,
					row=i_beat,
					padx=1,
					pady=2,
					sticky=tk.N+tk.E+tk.S+tk.W)
			self.current_beat_labels.append(self.beat_display[-1][0])

	def set_current_beat(self, beat_list: List[int]):
		assert len(beat_list) == len(self.beat_display)

		for i in self.current_beat_labels:
			i.config(bg='black')
		self.current_beat_labels.clear()

		for i_metre, val in enumerate(beat_list):
			label = self.beat_display[i_metre][val]
			label.config(bg='red')
			self.current_beat_labels.append(label)

	def _beat_frame_clear(self):
		self.beat_display.clear()
		for widget in self.beat_frame.winfo_children():
			widget.destroy()

		column_n, row_n = self.beat_frame.grid_size()
		for i in range(column_n):
			self.beat_frame.columnconfigure(i, weight=0)
		for i in range(row_n):
			self.beat_frame.rowconfigure(i, weight=0)

	def mainloop(self):
		self.window.mainloop()
