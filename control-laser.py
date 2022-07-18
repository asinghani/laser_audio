import libm2k
import time
import numpy as np
import resampy
from scipy.io import wavfile

SIGNAL_GENERATOR_RATE = 7500
ANALOG_IN_RATE = 10000
AUDIO_RATE = 44100

orig_rate, audio_for_laser = wavfile.read("okgoogle-time.wav")
audio_for_laser = audio_for_laser[len(audio_for_laser) // 25:]
audio_for_laser = resampy.resample(audio_for_laser, orig_rate, SIGNAL_GENERATOR_RATE)
audio_for_laser = audio_for_laser.astype(np.float32)

NUMSTD = 1.5
m = np.mean(audio_for_laser)
sd = np.std(audio_for_laser)
audio_for_laser[audio_for_laser > (m + NUMSTD*sd)] = m + NUMSTD*sd
audio_for_laser[audio_for_laser < (m - NUMSTD*sd)] = m - NUMSTD*sd

audio_for_laser = audio_for_laser / (NUMSTD * sd)
audio_for_laser = (audio_for_laser + 1.0) / 2
audio_for_laser = (audio_for_laser*5.0)

ctx = libm2k.m2kOpen()


ctx.calibrateADC()
ctx.calibrateDAC()

ain = ctx.getAnalogIn()
aout = ctx.getAnalogOut()

aout.setSampleRate(0, SIGNAL_GENERATOR_RATE)
aout.enableChannel(0, True)
aout.setCyclic(True)
aout.push([np.array(list(audio_for_laser) + len(audio_for_laser) * [4]).astype(np.float64)])


