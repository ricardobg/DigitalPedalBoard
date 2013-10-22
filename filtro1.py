# -*- coding: utf-8 -*-
"""
Filtro - Exemplo 1
"""
from audiolazy import *

rate = 44100 # Taxa de amostragem padrão (amostras/segundo)
s,Hz = sHz(rate)

# Sem efeito
gravador = AudioIO()
tocador = AudioIO()
minhaStream = gravador.record()
tocador.play(minhaStream)
stop = raw_input("Pressione ENTER para parar: ")
tocador.close()


# Aplicando um passa-baixas

def passa_baixas (fc,samplingfreq=44100):
    k = tan(pi*fc/samplingfreq)
    b0 = k/(k+1)
    b1 = k/(k+1)
    a1 = (k-1)/(k+1)
    filt = (b0 + b1*z**-1) / (1 + a1*z**-1)
    return filt
    
filtro = passa_baixas(800) # Criamos o passa baixas
tocador = AudioIO()
tocador.play(filtro(minhaStream))
stop = raw_input("Pressione ENTER para parar: ")
tocador.close()

# Outra forma de aplicar um filtro: Multiplicação por senóide !
senoide = sinusoid(700*Hz) # Criamos o passa baixas
tocador = AudioIO()
tocador.play(senoide * minhaStream)
stop = raw_input("Pressione ENTER para parar: ")
tocador.close()
gravador.close()


# O filtro era de fato um passa-baixas ?

filtro.plot(mag_scale="linear",rate=s)