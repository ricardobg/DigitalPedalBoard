# -*- coding: utf-8 -*-

import serial, threading
from audiolazy import ControlStream

class SerialData (threading.Thread):
    """
    Classe para ler os dados enviados pela porta serial pelo Arduino
    

    Seu atributo pedal contem um ControlStream usado para alterar parâmetros "on the fly" de algum filtro
    O atributo é
    """
    def __init__(self, porta='COM8', data_rate=9600, padrao_pedaleira=0.5, func_proximo=None
                 , func_anterior=None, limiar_superior_pedal=3.5, limiar_inferior_pedal=0.1):
        """
        Inicia a leitura dos dados assim como a porta
        porta: A porta Serial em que o Arduino está
        data_rate: quantos bits/segundo devem ser lidos
        padrao_pedaleira: Valor padrão para o pedal de expressão quando ele esta desligado
        func_proximo: Função que muda para o próximo filtro
        func_anterior: Função que muda para o filtro anterior
        limiar_superior_pedal: Valor máximo recebido que o pedal pode assumir
        limiar_inferior_pedal: Valor mínimo, abaixo desse valor usamos o padrao_pedaleira como entrada
        """        
        try:
            self.padrao_pedal = padrao_pedaleira
            self.pedal = ControlStream(self.padrao_pedal)
            self.proximo = func_proximo
            self.anterior = func_anterior
            self.limiar_superior_pedal = limiar_superior_pedal
            self.limiar_inferior_pedal = limiar_inferior_pedal
            self.kill_thread = False
            self.pause_thread = False    
            self.serial = serial.Serial(porta,data_rate)
        except:
            self.pedal = ControlStream(self.padrao_pedal)
            self.kill_thread = True
        threading.Thread.__init__(self)
    def run(self):
        while True:     
            if self.kill_thread:
                try:
                    self.serial.close()
                except:
                    pass
                return
            linha = self.serial.readline().strip().split(",")
            if len(linha) != 2:
                continue;
            ident,valor = tuple(linha)
            ident = int(ident)
            valor = int(valor)
            estado = 0
            if ident == 1:
                estado = valor
            elif ident == 2:
               self.pedal.value = (float(valor)/(1023.0))
            if self.pause_thread:
                return
            if estado == 1 and self.proximo is not None:
                self.proximo()
            elif estado == 2 and self.anterior is not None:
                self.anterior()        
           # print ident,valor
    def pause(self):
        """
        Pausa a Thread
        """
        self.pause_thread = True
    def __del__(self):
        self.kill_thread = True
        self.kill()
    def resume(self):
        """
        Resume a execução da Thread
        """
        self.pause_thread = False
        threading.Thread.__init__(self)
        self.start()
    def kill(self):
        """
        Termina a Thread e fecha a conexao com a porta serial
        """
        self.kill_thread = True
                 
#objeto = SerialData()
#objeto.start()

