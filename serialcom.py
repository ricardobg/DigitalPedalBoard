# -*- coding: utf-8 -*-
# This file is part of DigitalPedalBoard python program.
# Copyright (C) 2013 Copyright (C) 2013 Daniel Ken Fujimori Killner,
# Gabriel Moura Vieira Martinez, Rafael Alves de Araujo Sena,
# Ricardo Boccoli Gallego, Danilo de Jesus da Silva Bellini.
#
# DigitalPedalBoard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import serial, threading
from audiolazy import ControlStream

class SerialData (threading.Thread):
    """
    Classe para ler os dados enviados pela porta serial pelo Arduino
    Seu atributo pedal contem um ControlStream usado para alterar parâmetros "on the fly" de algum filtro
    """
    
   
    def __init__(self, porta='COM8', data_rate=9600, padrao_pedaleira=0.1, func_proximo=None
                 , func_anterior=None, limiar_superior_pedal=650):
        """
        Inicia a leitura dos dados assim como a porta
        
        porta: A porta Serial em que o Arduino está.
        Usando Windows:  Em Gerenciador de Dispositivos -> Portas (COM e LPT) Veja o nome em parênteses
        Usando Linux dmesg | grep tty, coloque porta como /dev/tty..        
        
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
               if valor == 0:
                   self.pedal.value = self.padrao_pedal
               else:
                    self.pedal.value = (float(valor)/(self.limiar_superior_pedal))
               
            if self.pause_thread:
                return
            if ident == 1 and estado == 1 and self.proximo is not None:
                self.proximo()
            elif ident == 1 and estado == 2 and self.anterior is not None:
                self.anterior()        
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

