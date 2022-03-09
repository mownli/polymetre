#!/usr/bin/env python3
import pkgutil
from typing import List

import numpy as np

from polymetre.linked_list import LinkedList


class AudioData:

	# audio_path_1 = 'resources/1.npy'
	# audio_path_2 = 'resources/2.npy'

	sample_rate = 44100
	bit_depth = np.int16
	channel_n = 1

	def __init__(self, metre_list: List[int], bpm: int):
		# self.audio_1: np.array = np.load(self.audio_path_1)
		# self.audio_2: np.array = np.load(self.audio_path_2)

		# with open('1fff' ,'wb') as f:
		# 	f.write(self.audio_1.tobytes())
		# with open('2fff' ,'wb') as f:
		# 	f.write(self.audio_2.tobytes())

		self.audio_1: np.array = np.frombuffer(pkgutil.get_data(__name__, 'resources/1_64'), dtype=np.int64)
		self.audio_2: np.array = np.frombuffer(pkgutil.get_data(__name__, 'resources/2_64'), dtype=np.int64)

		self.metre_list: List[int] = metre_list  # Should be ordered
		self.metre_list.sort()
		self.bpm: int = bpm

		self.frame: np.array = None
		self.intervals: List[LinkedList] = []

		self._compute()

	def reload(self, sample_rate: int, metre_list: List[int], bpm: int, dtype: np.dtype = np.int16) -> None:
		self.sample_rate = sample_rate
		self.bit_depth = dtype
		self.metre_list = metre_list
		self.metre_list.sort()
		self.bpm = bpm
		self._compute()

	def _compute(self) -> None:
		assert self.metre_list[0] > 0
		frame_len = int(self.sample_rate * self.metre_list[0] / (self.bpm / 60))
		self.frame = self._make_frame(self.metre_list, frame_len)
		self.intervals = self._make_intervals(self.metre_list, frame_len)

	def _make_beat_len_list(self, metre_list:List[int], frame_len: int) -> List[int]:
		ret: List[int] = []
		for i in metre_list:
			ret.append(int(frame_len / i))
		return ret

	def _make_frame(self, metre_list: List[int], frame_len: int) -> np.array:
		beat_len_list = self._make_beat_len_list(metre_list, frame_len)
		ret: np.array = np.zeros(frame_len, dtype=self.bit_depth)

		beat_sample_list = []
		for i_metre in range(len(metre_list)):
			if i_metre == 0:
				chosen_sample = self.audio_1
			else:
				chosen_sample = self.audio_2

			diff = beat_len_list[i_metre] - len(chosen_sample)
			if diff > 0:
				beat_sample_list.append(
					np.concatenate(((chosen_sample / len(metre_list)).astype(self.bit_depth), np.zeros(diff, dtype=self.bit_depth))))
			else:
				beat_sample_list.append(
					(chosen_sample[:beat_len_list[i_metre]] / len(metre_list)).astype(self.bit_depth))

		for i_metre, beats_n in enumerate(self.metre_list):
			for i_beat in range(beats_n):
				start = i_beat * len(beat_sample_list[i_metre])
				end = start + len(beat_sample_list[i_metre])
				ret[start:end] += beat_sample_list[i_metre]
				# for num, val in enumerate(range(start, start + len(beat_sample_list[i_metre]))):
				# 	ret[val] += beat_sample_list[i_metre][num]
		return ret

	def _make_intervals(self, metre_list: List[int], frame_len: int) -> List[LinkedList]:
		ret: List[LinkedList] = []
		for i_metre, metre in enumerate(metre_list):
			ret.append(LinkedList())
			beat_len = int(frame_len / metre)
			for beat_num in range(metre):
				start = beat_num * beat_len
				end = start+beat_len if beat_num != metre-1 else frame_len
				ret[i_metre].append((start, end))

		# Make the list cyclic
		for item in ret:
			item.tail.next = item.head

		return ret
