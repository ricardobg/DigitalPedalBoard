# -*- coding: utf-8 -*-
"""
Arquivo que cuida da execução do Áudio, assim como a aplicação dos filtros
"""

from audiolazy import *
import filters

# From https://github.com/danilobellini/audiolazy/blob/master/examples/keyboard.py
class ChangeableStream(Stream):
  """
  Stream that can be changed after being used if the limit/append methods are
  called while playing. It uses an iterator that keep taking samples from the
  Stream instead of an iterator to the internal data itself.
  """
  def __iter__(self):
    while True:
      yield next(self._data)



class Player():
    """
    Class Player, gerencia um player de Audio.
    É destruído no STOP.
    Ao pausar apenas para de exibir novos valores
    
    """
    def __init__(self, lista_filtros, pos=0, ncanais=1,rate=44100):
        """
        Inicia o Player.
        lista_filtros: lista de filtros aplicados, se for uma tupla, se trata
        de uma preset, caso contrário, nao.
        """
        self.filtros = lista_filtros
        self.posicao = pos
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
        ms = 1e-3 * filters.s
        self.release = 50 * ms
        self.rate = rate
        self.player = AudioIO(False)
        self.streamix = Streamix()
        self.input =  (self.player.record(nchannels=ncanais,rate=rate))
        self.stream = ChangeableStream(self.filter(self.input))
        self.streamix.add(0, self.stream)
        self.player.play(self.stream)
        
      
    def muda_filtro(self, novos_filtros):
        novo_filtro = CascadeFilter(novos_filtros)
        last = self.stream.take()
        self.stream.limit(0).append(line(self.release,last,0))
        self.filter = novo_filtro
        self.stream = ChangeableStream(self.filter(self.input))
        self.streamix.add(0,self.stream)
        
    def next_filter(self):
        if self.tipo == 1 or len(self.filtros) == 0:
            return
        self.posicao += 1
        if len(self.filtros) == self.posicao:
            self.posicao = 0
        self.muda_filtro(self.filtros[posicao])

    def previous_filter(self):
        if self.tipo == 1 or len(self.filtros) == 0:
            return
        self.posicao -= 1
        if self.posicao == -1:
            self.posicao = len(self.filtros)-1
        self.muda_filtro(self.filtros[posicao])
        
    def pausar (self):
        self.player.close()
    def tocar (self, lisa_filtros):
        if lista_filtros is None:
            lista_filtros = self.filtros
        self.__init__(lista_filtros,pos=self.posicao,ncanais=self.ncanais,rate=self.rate)
        
        
        
        