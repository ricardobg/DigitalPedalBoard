# -*- coding: utf-8 -*-

import serial, threading, time
from audiolazy import *

class SerialData (threading.Thread):
    """
    Classe para ler os dados enviados pela porta serial pelo Arduino
    porta: A porta Serial em que o Arduino está
    data_rate: quantos bits/segundo devem ser lidos
    padrao_pedaleira: Valor padrão para o pedal de expressão quando ele esta desligado
    func_proximo: 
    
    Seu atributo pedal contem um ControlStream usado para "controlar" algum filtro
    
    
    """
    def __init__(self, porta='COM6', data_rate=9600, padrao_pedaleira=0.5, func_proximo=None, func_anterior=None, limiar_superior_pedal=3.5,limiar_inferior_pedal=0.1):
        self.serial = serial.Serial(porta,data_rate)
        self.padrao_pedal = padrao_pedaleira
        self.pedal = ControlStream(self.padrao_pedal)
        self.proximo = func_proximo
        self.anterior = func_anterior
        self.limiar_superior_pedal = limiar_superior_pedal
        self.limiar_inferior_pedal = limiar_inferior_pedal
        threading.Thread.__init__(self)
    def run(self):
        while True:
         #   print self.serial.readline().split()[0].split(",")
             estado, valor_pedal = tuple(self.serial.readline().strip().split(","))
             estado = int(estado)
             if estado == 1:
                 func_proximo()
             elif estado == 2:
                 func_anterior()
             valor_pedal = float(valor_pedal)/self.limiar_superior_pedal
             if valor_pedal < self.limiar_inferior_pedal:
                 valor_pedal = self.padrao_pedaleira
             self.pedal.value = valor_pedal
             
             print self.pedal.value, estado
       
#objeto = SerialData()
#objeto.start()

