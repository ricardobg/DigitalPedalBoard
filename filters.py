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

"""
File to keep the created filters (effects).
Every filter is an 'Filtro' instance which contains the function that process
the input and other informations, like parameters, name and if it uses the
expression pedal.
"""
from audiolazy import *
rate = 44100
s,Hz = sHz(rate)


@tostream
def envoltoria(sig,alpha=.9999):
    """
    Returns the envelop of the signal with exponential decay.
    """
    last = 0.    
    for el in sig:
        if el < last: 
            last *= alpha
            yield last
        else:
            last = el
            yield last



"""
Functions that return a Stream followed by the function which instantiates the
filter with its parameters, name, etc.
"""

# DELAYS


def echo (sig, echo_time):
    sig = thub(sig/2, 2)
    smixer = Streamix()
    smixer.add(0,sig)
    smixer.add(echo_time*s,sig)
    return smixer
def eco(delay=0.001):
    """
    Returns an echo filter.
    Your signal in the time t is: I(t) + I(t-delay), where I() is your input
    signal.
    """
    dic = {u"Delay (s)":(0.2,float,(0,5))}
    inst = Filtro(echo, dic, u"Echo")
    inst.vparams[0] = delay
    return inst

@tostream
def the_flang(sig, freq, lag):
    posicao = lambda senoide: int((lag*s/2000.0)*(senoide+1))
    senoide = sinusoid(freq*Hz,phase=-pi/2)  
    ms = 1e-3*s
    lista = zeros().take(lag * ms + 1) 
    tam = len(lista)-1
    for el,v in izip(sig,senoide):
        lista.append(el)
        lista.pop(0)
        yield (el + lista[tam-posicao(v)])/2
def o_flanger(freq=0.3,lag=2):
    """
    Flanger effect.
    Its like the echo, but the delay time varies sinusoidally.
    """
    dic = {u"Frequency (mHz)":(.3,float,(.01,5))
        , u"Lag (ms)":(2,float,(1,50))}
    inst = Filtro(the_flang, dic, u"Flanger")
    inst.vparams[0] = freq
    inst.vparams[1] = lag
    return inst
    
def delay_variavel(sig, freq_var, lag=2.):
    posicao = lambda valor: int((lag*s/1000.0)*(valor))
    ms = 1e-3*s
    lista = zeros().take(lag * ms + 1) 
    tam = len(lista)-1
    for el,v in izip(sig,freq_var):
        lista.append(el)
        lista.pop(0)
        yield (el + lista[tam-posicao(v)])/2
def filtro_delay_variavel(lag=2.):
    """
    Variable echo. The delay time is as big as the expression pedal is
    pressed.
    """
    dic = {u"Lag (ms)":(2.,float,(1,50))}
    inst = Filtro(delay_variavel, dic, u"Variable Echo",True)
    inst.vparams[0] = lag
    return inst
    

# Basic Filters

@tostream
def amp(sig, ganho, ganho_max):
     for el in sig:
         ret = el*(next(iter(ganho))*ganho_max)            
         if builtins.abs(ret) > 1: yield el/builtins.abs(el)
         else: yield ret
def amplificador(ganho_max=5.0):
    """
    Amplifier. Its gains varies with the expression pedal.
    """    
    dic = {u"Maximum gain":(5.0,float,(0.1,10))}
    inst = Filtro(amp, dic, u"Amplifier", True)
    inst.vparams[0] = ganho_max
    return inst
    
def low_pass (signal, cutoff):
        filt = lowpass(cutoff/(float(cutoff)))
        return filt(signal)
def passa_baixas(cutoff=700):
    """ 
    Low pass filter (It mitigates high frequencies)
    """
    dic = {u"Cutoff frequency (Hz)":(700,int,(0,20000))}
    inst = Filtro(low_pass, dic, u"Low Pass")
    inst.vparams[0] = cutoff
    return inst


def high_pass (signal,cutoff):
        filt = highpass(cutoff*Hz)
        return filt(signal)
def passa_altas(cutoff=700):
    """  
    High pass filter (It mitigates low frequencies)
    """
    dic = {u"Cutoff frequency (Hz)":(700,int,(0,20000))}
    inst = Filtro(high_pass, dic, u"High Pass")
    inst.vparams[0] = cutoff
    return inst
    
def all_pass (signal, cutoff):
        c = (tan(cutoff*pi/rate) - 1)/(tan(cutoff*pi/rate) + 1)
        filt = (z**-1 + c)/(1 + c*z**-1)
        return filt(signal)
def passa_tudo(cutoff=700):
    """ 
    All pass filter. It doesn't mitigate any frequency, but changes its phase.
    Useful when creating a phaser.
    """
   
    dic = {u"'Cutoff frequency'  (Hz)":(700,int,(0,20000))}
    inst = Filtro(all_pass, dic, u"All Pass")
    inst.vparams[0] = cutoff
    return inst
    
    
    
# LIMITERS
    
def the_limiter(sig,threshold):
        sig = thub(sig, 2)
        return sig * Stream( 1. if el <= threshold else threshold / el
               for el in envoltoria(sig) )

def limitador(threshold=.5):
    """ 
    Limiter filter. It bounds the envelop of your signal between 
    -thereshold and +thereshold.
    """
    dic = {u"Threshold":(.5,float,(0,1))}
    inst = Filtro(the_limiter, dic, u"Limiter")
    inst.vparams[0] = threshold
    return inst

def the_compressor(sig,threshold,slope):
        sig = thub(sig, 2)
        return sig * Stream(1. if el <= threshold 
        else (slope + threshold*(1 - slope)/el) for el in envoltoria(sig))
def compressor(threshold=.5, slope=.5):
    """ 
    Above the threshold, it mitigates the signal with a tangent.
    """
    dic = {u"Threshold":(.5,float,(0,1)),
           u"Tangent":(.5,float,(0,1))}
    inst = Filtro(the_compressor, dic, u"Compressor")
    inst.vparams[0] = threshold
    inst.vparams[1] = slope
    return inst

def expander(sig,threshold,slope):
      sig = thub(sig, 2)
      return sig * Stream((slope + threshold*(1 - slope)/el) 
      if (el <= threshold and el > 0) else 1. for el in envoltoria(sig))

def filtro_expander(threshold=.5, slope=.5):
    """ 
    If you are strict, this isn't an expander because it should increase the 
    signal above a threshold. But this filter mitigates the signal below
    the threshold with a tangent.    
    """
    dic = {u"Threshold":(.5,float,(0,1)),
           u"Tangent":(.5,float,(0,1))}
    inst = Filtro(expander, dic, u"Expander")
    inst.vparams[0] = threshold
    inst.vparams[1] = slope
    return inst
    
    
# DISTORTIONS
  
@tostream
def distwire(sig,threshold):
    for el in sig:
        if builtins.abs(el) < threshold: yield el
        else: yield el/builtins.abs(el) - el
def dist_wire(threshold=.5):
    """ 
    Wire Distortion.
    We made this up, it reverses your signal above a threshold.
    """
    dic = {u"Threshold":(.5,float,(0,1))}
    inst = Filtro(distwire, dic, u"Distwire")
    inst.vparams[0] = threshold
    return inst

def senoide(sig,freq):
    return sig*sinusoid(freq*Hz)    
def filtro_senoide(freq=700):
    """ 
    Multiplies your signal by a sinusoid.
    """
    dic = {u"Frequency (Hz)":(700,float,(0,20000))}
    inst = Filtro(senoide, dic, u"Sinusoid")
    inst.vparams[0] = freq
    return inst

def senoide_var(sig,freq,freq_max):
    return sig*sinusoid(freq*freq_max*Hz)    
def filtro_senoide_var(freq_max=10000):
    """ 
    Ring modulation effect.    
    It multiplies your signal by a variable sinusoid. The sinusoid's frequency
    varies with the expression pedal.
    """
    dic = {u"Maximum Frequency(Hz)":(10000,float,(0,20000))}
    inst = Filtro(senoide_var, dic, u"Ring modulation",True)
    return inst

@tostream
def corta_var(sig, corta, limite):
    for el,v in izip(sig,corta):
        if v > limite: yield 0.
        else: yield el
def filtro_corta(limite=.5):
    """ 
    Cuts the sound above a threshold.
    """
    dic = {u"Threshold":(.5,float,(0,1))}
    inst = Filtro(corta_var, dic, u"Cut",True)
    return inst


def mult_env(sig,alpha):
    return sig * envoltoria(sig,alpha)

def filtro_mult_env(alpha=.9999):
    """ 
    Multiplies your signal by its envelop.
    """
    dic = {u"Alpha":(.9999,float,(0.1,.999999))}
    inst = Filtro(mult_env, dic, u"Envelop",False)
    return inst

def the_resonator (signal,freq,band):
    res = resonator(freq*Hz,band*Hz)
    return res(signal)
    
def filtro_res(freq=900,band=5):
    """
    Resonator effect.
    When playing some chords, the output oscillates.
    """
    dic = {u"Frequency (Hz)":(900,float,(0,20000))
    , u"Bandwidth (Hz)": (5,float,(1,100))}
    inst = Filtro(the_resonator, dic, u"Resonator",False)
    return inst
    
# ControlStream that contains the expression pedal value.
pedal = ControlStream(0.1)
     
class Filtro:
    """ 
    Filters class.
    params: It contains the dictionary that distinguish the filter.
    vparams: Default values for the parameters.
    name: Filter's name.
    usa_pedal: Indicates whether the expression pedal will be used or not.
      
    """
    def __init__(self, fun, dic, name, usa_pedal=False):
        """        
        fun: The function which process the input and returns an output.
        dic: Dictionary which names every filter parameter and its value is a
        tuple that contains (default_value, data_type, (min_value,max_value)).
        name: The filter's name.
        
        The filtros variable contains a dictionary defined by the filters
        group and a tuple with the filters function.
        """
        self.params = dic
        self.__fun = fun
        self.vparams = [valor[0] for valor in dic.values()]
        self.name = name
        self.usa_pedal=usa_pedal
   
    def __call__ (self, sig):
        if not self.usa_pedal:
            return (self.__fun(sig, *(tuple(self.vparams))))
        else:
            return (self.__fun(sig, pedal, *(tuple(self.vparams))))


    filtros = {u"Basic Effects": (passa_altas,passa_baixas,passa_tudo, amplificador, filtro_corta)
            , u"Limiters": (limitador,compressor,filtro_expander)
    
                , u"Distortions": (dist_wire,filtro_senoide_var,filtro_senoide, filtro_mult_env, filtro_res)
                , u"Delays": (eco, filtro_delay_variavel, o_flanger)                
                }
        