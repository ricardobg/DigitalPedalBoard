# -*- coding: utf-8 -*-
"""
Arquivo que cuida da execução do Áudio, assim como a aplicação dos filtros
"""

from audiolazy import *
import filters

class Player():
    """
    Class Player, gerencia um player de Audio.
    É destruído no STOP.
    Ao pausar apenas para de exibir novos valores
    
    """
    def __init__(self, lista_filtros, ncanais=1,rate=44100):
        """
        Inicia o Player.
        lista_filtros: lista de filtros aplicados, se for uma tupla, se trata
        de uma preset, caso contrário, nao.
        """
        self.filtros = lista_filtros
        self.posicao = 0
        if lista_filtros is tuple:  
            print "tupla"
            self.tipo = 0
            if len(self.filtros) != 0:
                self.filter = CascadeFilter(self.filtros[0])
            else:
                self.filter = CascadeFilter()
            
        else:
            self.tipo = 1
            self.filter = CascadeFilter(self.filtros)
        self.ncanais = ncanais
        self.rate = rate
        self.player = AudioIO(False)    
        self.input = self.player.record(nchannels=ncanais,rate=rate)
        self.player.play(self.filter(self.input))
    
    def next_filter(self):
        if self.tipo == 1:
            return
        self.posicao += 1
        if len(self.filtros) == self.posicao:
            self.posicao = 0
        
        novo_player = AudioIO(False)
        novo_filtro = CascadeFilter(self.filtros[self.posicao])
        novo_input = novo_player.record(nchannels=self.ncanais,rate=self.rate)
        
        self.player.close()
        novo_player.play(novo_filtro(novo_input))
        
        self.player = novo_player
        self.input = novo_input
        self.filter = novo_filtro
    def previous_filter(self):
        if self.tipo == 1:
            return
        self.posicao -= 1
        if self.posicao == -1:
            self.posicao = len(self.filtros)-1
        
        novo_player = AudioIO(False)
        novo_filtro = CascadeFilter(self.filtros[self.posicao])
        novo_input = novo_player.record(nchannels=self.ncanais,rate=self.rate)
        
        self.player.close()
        novo_player.play(novo_filtro(novo_input))
        
        self.player = novo_player
        self.input = novo_input
        self.filter = novo_filtro
    def pausar (self):
        self.player.close()
    def tocar (self, lista_filtros=None):
        if lista_filtros is None:
            lista_filtros = self.filtros
        self.__init__(lista_filtros)
        
        
        
        