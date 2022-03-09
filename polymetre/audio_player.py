import threading

import numpy as np
import sounddevice as sd


class AudioPlayer:

	def __init__(self, data: np.array, channel_n: int, sample_rate: int, dtype: np.dtype):
		self.data = data
		self._head = 0
		self._mutex = threading.Lock()
		self.stream = sd.OutputStream(
			channels=channel_n,
			callback=self._callback,
			samplerate=sample_rate,
			dtype=dtype)
		self.muted = False

	def start(self) -> None:
		self.stream.start()

	def stop(self) -> None:
		self.stream.stop()

	def abort(self) -> None:
		self.stream.abort()
		self._head = 0

	def close(self) -> None:
		self.stream.close()
		self._head = 0

	def __del__(self):
		self.close()

	def _get_next_frame(self, buf_size) -> np.array:
		with self._mutex:
			assert self._head < len(self.data)
			start = self._head
			if self._head + buf_size >= len(self.data):
				self._head = buf_size - (len(self.data) - start)
				return np.concatenate((self.data[start:], self.data[:self._head])) if not self.muted else 0
			else:
				self._head = start + buf_size
				return self.data[start:self._head] if not self.muted else 0

	def _callback(self, data, frames, time, status):
		data[:, 0] = self._get_next_frame(len(data[:, 0]))

	def get_head(self, blocking=True) -> tuple[bool, int]:
		if self._mutex.acquire(blocking=blocking):
			ret = self._head
			self._mutex.release()
			return True, ret
		else:
			return False, 0

	def set_data(self, data: np.array) -> None:
		with self._mutex:
			self.data = data

	def set_head(self, head: int) -> None:
		with self._mutex:
			self._head = head
