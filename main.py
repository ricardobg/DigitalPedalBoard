"""
Arquivo para executar os filtro e testa-los
"""

import filters
from audiolazy import *
from scipy.io import wavfile


filename = "notas/si.wav"#raw_input("Type your .wav file location: ")
myrate, data_sound = wavfile.read(filename)
print myrate
s, Hz = sHz(myrate)
maximo = float(max(abs(data_sound.max()),abs(data_sound.min())))
data = Stream(data_sound)/maximo
player = AudioIO(False)
#player.play(data)
entrada = Stream(sinusoid(2*pi*2))
filt = filters.low_pass(2/3.0);
#entrada = filt(entrada)
player.play(entrada)

#filt = 1 / (1 - z*pi/2)
#filt2 = (1 + z*pi/2) / (1 - z*pi/2)

"""filt.plot(mag_scale="linear")
filt2.plot(mag_scale="linear")
data = thub(filt(data),3)
maximo1 = abs(max(data))
maximo2 = abs(min(data))
maximo = max(maximo1,maximo2)
print maximo1,maximo2,maximo
data = data / (maximo*1.0)
player.play(data)
"""


stop = raw_input("Press ENTER to stop ")
player.close()

