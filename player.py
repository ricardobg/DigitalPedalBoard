# -*- coding: utf-8 -*-
"""
Arquivo que cuida da execução do Áudio, assim como a aplicação dos filtros
"""

from audiolazy import *
import filters

# Classe adaptada de https://github.com/danilobellini/audiolazy/blob/master/examples/keyboard.py
class ChangeableStream(Stream):
  """
  Mudança na classe Stream para podermos zerar/limitar a Stream enquanto ela é tocada
  """
  def __iter__(self):
    while True:
      self.last = next(self._data)
      yield self.last

class MyStreamix(Streamix):
  """
  Mudança na classe Streamix para guardarmos o último valor
  """
  def __iter__(self):
    while True:
      self.last = next(self._data)
      yield self.last


class Player():
    """
    Classe Player, gerencia um player de Audio.
    É destruído no STOP.
    Ao pausar apenas para de exibir novos valores
    """
    
    def __init__(self, lista_filtros, pos=0, ncanais=1,rate=44100):
        """
        Inicia o Player.
        lista_filtros: lista de filtros aplicados, se for uma tupla, se trata
        de uma preset.
        pos: Posição Inicial no preset
        """
        self.filtros = lista_filtros
        self.posicao = pos
        if isinstance(lista_filtros, tuple):
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
        self.release = 1 * filters.s
        self.rate = rate
        self.player = AudioIO(False)
        self.streamix = MyStreamix()
        self.input =  ChangeableStream(self.player.record(nchannels=ncanais,rate=rate))
        self.dados = self.filter(self.input)
        self.stream = ChangeableStream(self.dados)
        self.stream.last = 0.0
        self.streamix.last = 0.0
        self.input.last = 0.0
        self.streamix.add(0, self.stream)
        
        self.player.play(self.streamix)
        
    def last_input_output(self):
        """
        Função que retorna os últimos valores de input e output
        Na forma de tupla (in,out)
        """
        if not self.player.finished:
            return (self.input.last,self.streamix.last)
        return (0.0,0.0)
    def muda_filtro(self, novos_filtros):
        """
        Muda o filtro aplicado, garantindo que não haja um "click" ao fazer isso
        """
        """
        if self.tipo == 1:
            self.filtros = novos_filtros
        novo_filtro = CascadeFilter(novos_filtros)
        last = self.stream.last
        self.stream.limit(0).append(line(self.release,last,0))
        self.filter = novo_filtro
        self.dados = self.filter(self.input)
        self.stream = ChangeableStream(self.dados)
        self.stream.last = 0.0
        self.streamix.add(0,self.stream)
        """
        novo_filtro = CascadeFilter(novos_filtros)
        self.filter = novo_filtro
        last = self.stream.last
        self.stream.limit(0).append(line(self.release,last,0))
        player2 = AudioIO(False)
        self.input = ChangeableStream(player2.record(nchannels=self.ncanais,rate=self.rate))
        self.input.last = 0.0
        self.dados = self.filter(self.input)
        self.stream = ChangeableStream(self.dados)
        self.stream.last = 0.0
        self.streamix.add(0,self.stream)
        
        self.player.close()  
        player2.play(self.streamix)
        self.player = player2
        
        
        
    def next_filter(self):
        """
        Muda para o próximo filtro do preset
        """
        if self.tipo == 1 or len(self.filtros) == 0:
            return
        self.posicao += 1
        if len(self.filtros) == self.posicao:
            self.posicao = 0
        self.muda_filtro(self.filtros[self.posicao])

    def previous_filter(self):
        """
        Muda para o filtro anterior do preset
        """
        if self.tipo == 1 or len(self.filtros) == 0:
            return
        self.posicao -= 1
        if self.posicao == -1:
            self.posicao = len(self.filtros)-1
        self.muda_filtro(self.filtros[self.posicao])
    
    def __del__(self):
        if not self.player.finished:
            self.player.close()
    def pausar (self):
        """
        Para o player
        """
        if not self.player.finished:
            self.player.close()

    def tocar (self, lista_filtros=None):
        """
        Reinicia o player (tanto quando ele é pausado como parado)
        """
        if lista_filtros is None:
            lista_filtros = self.filtros
        self.__init__(lista_filtros,pos=self.posicao,ncanais=self.ncanais,rate=self.rate)
        
        
        
        