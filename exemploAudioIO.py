# -*- coding: utf-8 -*-
"""
Exemplo AudioIO

"""
from audiolazy import *

senoide = sinusoid(pi/40)
senoide2 = sinusoid(pi/90)
player = AudioIO() # Inicia o player (que pode tanto gravar como reproduzir som)
player.play(senoide+senoide2) # Toca uma Stream
stop = raw_input("Pressione ENTER para parar o som")
player.close()
