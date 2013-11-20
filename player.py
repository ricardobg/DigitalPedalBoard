# -*- coding: utf-8 -*-
"""
Arquivo que cuida da execução do Áudio, assim como a aplicação dos filtros
"""

from audiolazy import Stream, Streamix, AudioIO, CascadeFilter, line, chunks
import filters
#chunks.size = 256

# Classe adaptada de https://github.com/danilobellini/audiolazy/blob/master/examples/keyboard.py
class ChangeableStream(Stream):
  """
  Mudança na classe Stream para podermos zerar/limitar a Stream enquanto ela é tocada
  """
  def __iter__(self):
    while True:
      self.last = next(self._data)
      yield self.last 
      
ms = 1e-3 * filters.s
class Player:
    """
    Classe Player, gerencia um player de Audio.
    É destruído no STOP.
    Ao pausar apenas para de exibir novos valores
    """
   
    def __init__(self, lista_filtros, ncanais=1,rate=44100):
        """
        Inicia o Player.
        lista_filtros: lista de filtros aplicados, se for uma tupla, se trata
        de uma preset.
        pos: Posição Inicial no preset
        """
       
        self.filtros = lista_filtros
        if self.filtros is not None:
            self.filter = CascadeFilter(self.filtros)
        else:
            self.filter = CascadeFilter()
        self.ncanais = ncanais
       
        self.release = 0.05*filters.s
        self.rate = rate
        self.player = AudioIO()
        self.streamix = Streamix(True)
        self.input = ChangeableStream(self.player.record(nchannels=ncanais,rate=self.rate))
        self.input.last = 0.
        self.stream = ChangeableStream(self.filter(self.input))
        self.stream.last = 0.
        self.player.play(self.streamix, rate=self.rate)        
        self.streamix.add(0,self.stream)
        
        
        #tk = tkinter.Tk()
        
        
    def last_input_output(self):
        """
        Função que retorna os últimos valores de input e output
        Na forma de tupla (in,out)
        """
        try:
           return (self.input.last, self.stream.last)
        except:
            return (0,0)
    def muda_filtro(self, novos_filtros, window):
        """
        Muda o filtro aplicado, garantindo que não haja um "click" ao fazer isso
        """
        #self.chamando = True
        novo_filtro = CascadeFilter(novos_filtros)
        last = self.stream.last
        self.stream.limit(0).append(line(self.release,last,0))      
                
        self.stream = ChangeableStream(novo_filtro(self.input))
        self.stream.last = last
        self.streamix.add(0, self.stream)  
        
    def __del__(self):
        if not self.player.finished:
            self.player.close()
            #self.playerGrava.close()
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
        self.__init__(lista_filtros,ncanais=self.ncanais,rate=self.rate)
        
        
        
        