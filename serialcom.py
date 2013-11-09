# -*- coding: utf-8 -*-

import serial, threading, time
from audiolazy import *

class SerialData (threading.Thread):
    """
    Classe para ler os dados enviados pela porta serial pelo Arduino
    
    porta: A porta Serial em que o Arduino está
    data_rate: quantos bits/segundo devem ser lidos
    padrao_pedaleira: Valor padrão para o pedal de expressão quando ele esta desligado
    func_proximo: Função que muda para o próximo filtro
    func_anterior: Função que muda para o filtro anterior
    limiar_superior_pedal: Valor máximo recebido que o pedal pode assumir
    limiar_inferior_pedal: Valor mínimo, abaixo desse valor usamos o padrao_pedaleira como entrada
    
    Seu atributo pedal contem um ControlStream usado para alterar parâmetros "on the fly" de algum filtro
    O atributo é
    """
    def __init__(self, porta='COM6', data_rate=9600, padrao_pedaleira=0.5, func_proximo=None
                 , func_anterior=None, limiar_superior_pedal=3.5, limiar_inferior_pedal=0.1):
        self.serial = serial.Serial(porta,data_rate)
        self.padrao_pedal = padrao_pedaleira
        self.pedal = ControlStream(self.padrao_pedal)
        self.proximo = func_proximo
        self.anterior = func_anterior
        self.limiar_superior_pedal = limiar_superior_pedal
        self.limiar_inferior_pedal = limiar_inferior_pedal
        self.kill_thread = False
        self.pause_thread = False    
        threading.Thread.__init__(self)
    def run(self):
        while True:     
            if self.kill_thread:
                try:
                    self.serial.close()
                except:
                    pass
                return
            valores = self.serial.readline().strip().split(",")
            if len(valores) != 2:
                continue
            estado, valor_pedal = tuple(valores)
            estado = int(estado)
            valor_pedal = float(valor_pedal)/self.limiar_superior_pedal
            if self.pause_thread:
                return
            if estado == 1 and self.proximo is not None:
                self.proximo()
            elif estado == 2 and self.anterior is not None:
                self.anterior ()
           
            if valor_pedal < self.limiar_inferior_pedal:
                valor_pedal = self.padrao_pedaleira
            self.pedal.value = valor_pedal
            #print self.pedal.value, estado
    def pause(self):
        """
        Pausa a Thread
        """
        #time.sleep(3600*24*30*30)
    
        #threading.Thread._Thread__stop(self)
        self.pause_thread = True
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

