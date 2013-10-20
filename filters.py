# -*- coding: utf-8 -*-
from audiolazy import *
"""
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
def low_pass (cutoff,samplingfreq=44100):
    k = tan(pi*cutoff/samplingfreq)
    b0 = k/(k+1)
    b1 = k/(k+1)
    a1 = (k-1)/(k+1)
    filt = (b0 + b1*z**-1) / (1 + a1*z**-1)
    return filt

"""
b0 = 1/(k+1)
b1 = -1/(k+1)
a1 = (k-1)/(k+1)
"""
def high_pass (cutoff,samplefreq=44100):
    k = tan(pi*cutoff/samplefreq)
    b0 = 1/(k+1)
    b1 = -1/(k+1)
    a1 = (k-1)/(k+1)
    filt = (b0 + b1*z**-1) / (1 + a1*z**-1)
    return filt


def all_pass (ars):
    pass

"""
Delay filter, output = delayed input
delay in samples
"""
def delay(delay=100):
    return  z**(-delay)


"""
Echo filter, output = input + delayed input
delay in samples
"""
def echo(delay=100):
    out = 1 + z**(-delay)
    return out
    
"""
G(z) = (b0 + b1*z**-1 + b2*z**-2) / (1 + a1*z**-1 + a2*z**-2)

"""
def resonator (freq,band,samplefreq=44100.0):
    res = resonator(2*pi*freq/samplefreq,2*pi*1000/samplefreq)
    return res


"""
G(z) = (b0 + b1*z**-1 + b2*z**-2) / (1 + a1*z**-1 + a2*z**-2)

"""
def limiter ():
    pass

def compressor (compressorSize):
    filt = z**0 / float(compressorSize)
    return filt
    

def expander():
    pass

def distortion ():
    pass

def phaser ():
    pass

def flanger ():
    pass
