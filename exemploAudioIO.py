# -*- coding: utf-8 -*-
"""
Exemplo AudioIO

"""
from audiolazy import *
senoide = sinusoid(pi/40)
player = AudioIO() # Inicia o player (que pode tanto gravar como reproduzir som)
player.play(senoide) # Toca uma Stream
stop = raw_input("Pressione ENTER para parar o som")
player.close()
