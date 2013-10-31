# -*- coding: utf-8 -*-
from audiolazy import *

rate = 44100
s,Hz = sHz(rate)



"""
Filters are defined in a Map:
{"internal name":[filter_name, filter_function, params_names, param_values]
Where param_values is a tuple that contains all parameters and its values  and param_names contains the names
rate - Samples/second
fs - sample rating
fc - cutoff frequency

Obs.:
fs = rate = (numero de amostras)/tempo = s**-1
para fc = rate -x = x 
Porque próximo à 2*pi, temos baixas frequências e longe de 2*pi ou perto de pi, altas frequências
"""

"""
allpass,lowpass,highpass:
G(z) = (b0 + b1*z**-1) / (1 + a1*z**-1)
k = tg (pi*fc/fs)
"""

"""
b0 = k/(k + 1)
b1 = k/(k+1)
a1 = (k-1)/(k+1)
"""

def low_pass (signal, cutoff):
    filt = lowpass(cutoff*Hz)
    return filt(signal)
    
def high_pass (signal,cutoff):
    filt = highpass(cutoff*Hz)
    return filt
  
def the_resonator (signal,freq,band):
    res = resonator(freq*Hz,band*Hz)
    return res(signal)
    
def the_limiter(sig,threshold):
  sig = thub(sig, 2)
  size=256
  env=envelope.rms
  cutoff=pi/2048
  return sig * Stream( 1. if el <= threshold else threshold / el
                       for el in maverage(size)(env(sig, cutoff=cutoff)) )


def expander(sig,threshold,slope):
      sig = thub(sig, 2)
      size=256
      env=envelope.rms
      cutoff=pi/2048
      return sig * Stream(slope if el <= threshold else 1.
                      for el in maverage(size)(env(sig, cutoff=cutoff)) )


def compressor(sig,threshold,slope):
      sig = thub(sig, 2)
      size=256
      env=envelope.rms
      cutoff=pi/2048
      return sig * Stream(1. if el <= threshold else slope
                      for el in maverage(size)(env(sig, cutoff=cutoff)) )
   
def echo (sig, echo_time):
    sig = thub(sig/2, 2)
    smixer = Streamix()
    smixer.add(0,sig)
    smixer.add(echo_time*s,sig)
    return smixer

def teste (samplefreq=44100):
      return (pi*samplefreq)/((pi*samplefreq)*2 + z**2)
    
def all_pass (ars):
    pass

                       

def distortion ():
    pass

def phaser ():
    pass

def flanger ():
    pass


digital_filters = {"lowpass": ["Passa-baixas",low_pass,("Frequência de Corte (Hz)"),(500)]
, "highpass": ["Passa-altas",high_pass,("Frequência de Corte (Hz)"),(800)]
, "ressonator": ["Ressonador",the_resonator,("Frequência Ressonante (Hz)","Tamanho da Banda (Hz)"),(800,100)]
, "limiter": ["Limitador",the_limiter,("Início (0-1)"),(0.5) ]
, "echo": ["Eco",echo,("Tempo de Eco (s)"),(0.05) ]
, "expander": ["Expansor",expander,("Fim (0-1), Fator (0-1)"),(0.5,0.001) ]
, "compressor": ["Compressor",compressor,("Início (0-1), Fator (0-1)"),(0.5,0.001) ]

    }
entrada = AudioIO()
saida = AudioIO()
inp = entrada.record()
output = echo(inp,0.5)
saida.play(output)
terminar = raw_input("Terminar")
saida.close()
entrada.close()



