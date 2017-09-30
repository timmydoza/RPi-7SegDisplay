import RPi.GPIO as GPIO
import multiprocessing
import signal
import sys
from time import sleep

class RPi_7SegDisplay():

    _CHARACTERS = {
        '0': 0b11000000,
        '1': 0b11111001,
        '2': 0b10100100,
        '3': 0b10110000,
        '4': 0b10011001,
        '5': 0b10010010,
        '6': 0b10000010,
        '7': 0b11111000,
        '8': 0b10000000,
        '9': 0b10010000,
        ' ': 0b11111111,
        '-': 0b10111111,
        '.': 0b01111111
        }

    _BLANK = [_CHARACTERS[' ']] * 8


    def __init__(self, data_pin, clock_pin, latch_pin):
        self._data = data_pin
        self._clock = clock_pin
        self._latch = latch_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([data_pin, clock_pin, latch_pin], GPIO.OUT)

        if (len(multiprocessing.active_children()) == 0):
            self._proc = multiprocessing.Process(target=self._display)
            self._proc.start()

        self._queue = multiprocessing.Queue(2)
        self._queue.put(_BLANK)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _shift(self, byte):
        for i in range(7, -1, -1):
            GPIO.output(self._data, byte & (1 << i))
            GPIO.output(self._clock, 1)
            GPIO.output(self._clock, 0)


    def _write(self, message):
        for i, char in enumerate(message):
            self._shift(1 << i)
            self._shift(char)
            GPIO.output(self._latch, 1)
            GPIO.output(self._latch, 0)
            sleep(0.003)


    def _display(self):
        while True:
            if not self._queue.empty():
                text = self._queue.get()
            self._write(text)


    def show(self, message):
        result = []
        if not self._queue.full():
            for i, char in enumerate(message):
                if (char == '.' and i > 0):
                    result[-1] -= 128
                elif (char != '.'):
                    result.append(self._CHARACTERS[char])
            self._queue.put(result)


    def stop(self):
        self._proc.terminate()
        self._write(_BLANK)
        GPIO.cleanup()

    def _signal_handler(self, signal, frame):
        stop()
        sys.exit(0)
