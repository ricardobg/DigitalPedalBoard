"""
Arquivo para executar os filtro e testa-los
"""

import filters
from audiolazy import *
from scipy.io import wavfile


filename = "notas/do.wav"#raw_input("Type your .wav file location: ")
myrate, data_sound = wavfile.read(filename)
#print myrate
s, Hz = sHz(myrate)
maximo = float(max(abs(data_sound.max()),abs(data_sound.min())))
data = Stream(data_sound)/maximo
player1 = AudioIO(False)
player2 = AudioIO(False)
valores = Stream(line(44100*1, 0, -1))
delay = 1 + valores * z ** -5 # Transformada Z do filtro
data2 = delay(thub(data,2))
#player1.play(data)
player2.play(data2)
stop = raw_input("Press ENTER to stop ")
#player1.close()
player2.close()


#splayer2 = AudioIO(False)
#player.play(data)
#entrada = Stream(sinusoid(2*pi*3.7/4.0))
#data2 = thub(data,2)
#out = filters.testfilter(data)

#out = out + data
#player1.play(out,chunk_size=16)
#filt.plot(mag_scale="linear",rate=44100)

#entrada = player1.play(filt(data))
#saida = player2.play(filt(entrada))


#filt.plot(mag_scale="linear")
#entrada = filt(entrada)
#player.play(entrada)

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

#seno = sinusoid(pi/2)

#filt = (z**2 + 2168727)/(z**2 + 125.8*z + 2168727)
#filt.plot(rate=44100)
#saida = filt(data)
#player1.play(saida)

"""res = filters.teste()
data = player1.record()
player2.play(res((data)))
stop = raw_input("Press ENTER to stop ")
player2.close()
player1.close()
res = filters.teste()
res.plot(rate=44100)
"""

#rate = 44100
#s, Hz = sHz(rate)
#sin = Stream(sinusoid(440*Hz))
#tr = (440*Hz)/((440*Hz)**2 + z**2)
#tr.plot(rate=rate,mag_scale="linear")