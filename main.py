"""
Arquivo para executar os filtro e testa-los
"""

import filters
from audiolazy import *
from scipy.io import wavfile

filename = "notas/do.wav"#raw_input("Type your .wav file location: ")
myrate, data_sound = wavfile.read(filename)
print myrate
s, Hz = sHz(myrate)
data = Stream(data_sound)/max(abs(data_sound.max()),abs(data_sound.min()))
player = AudioIO()
#player.play(data)

filt = filters.low_pass(1/8.0)
data2 = filt(data)
player.play(data2)