# -*- coding: utf-8 -*-
from audiolazy import *

rate = 44100
s,Hz = sHz(rate)

class Filtro:
    """ Classe para os filtros
        - O filtro deve conter: uma função que recebe um Stream e retorna outro Stream (além de outros parametros)
        - A função recebe um dicionário (dic) que dá um nome para cada parametro do filtro e 
        o seu valor é uma tupla que contém (valor_padrao, tipo, (valor_inicial,valor_final))
        - A variável params contém o dicionário acima
        - Já a variável out é a função que recebe Stream e retorna Stream
        - vparams é uma tupla com os valores dos parâmetros
        
        A variável estatica filtros contém um dicionário definido pelo grupo de filtros e por uma tupla contendo
        as funções que instanciam os filtros
    """
    def __init__(self, fun, dic, name):
        self.params = dic
        self.__fun = fun
        self.vparams = [valor[0] for valor in dic.values()]
        self.out = lambda sig: (fun(sig, *(tuple(self.vparams))))
        self.name = name
    
    def update_default(self):
        self.out = lambda sig: (self.__fun(sig, *(tuple(self.vparams))))
    @staticmethod
    def passa_baixas(cutoff=700):
        """ Filtro que atenua altas frequências
        """
        def low_pass (signal, cutoff):
            filt = lowpass(cutoff/(float(cutoff)))
            return filt(signal)
        dic = {u"Frquência de Corte (Hz)":(700,int,(0,20000))}
        inst = Filtro(low_pass, dic, "Passa Baixas")
        inst.vparams[0] = cutoff
        return inst
    
    @staticmethod
    def eco(delay=0.001):
        """ Retorna uma pnlinstância do Eco
        """
        def echo (sig, echo_time):
            sig = thub(sig, 2)
            smixer = Streamix()
            smixer.add(0,sig)
            smixer.add(echo_time*s,sig)
            return smixer
        dic = {u"Intervalo (s)":(0.2,float,(0,5))}
        inst = Filtro(echo, dic, "Eco")
        inst.vparams[0] = delay
        return inst
    
    @staticmethod
    def passa_altas(cutoff=700):
        """  Filtro que atenua baixas frequências
        """
        def high_pass (signal,cutoff):
            filt = highpass(cutoff*Hz)
            filt.plot()
            return filt(signal)
        dic = {u"Frquência de Corte (Hz)":(700,int,(0,20000))}
        inst = Filtro(high_pass, dic, "Passa Altas")
        inst.vparams[0] = cutoff
        return inst
        
    @staticmethod
    def passa_tudo(cutoff=700):
        """ Filtro que não muda a intensidade, apenas a fase da sua entrada
        """
        def all_pass (signal, cutoff):
            c = (tan(cutoff*pi/rate) - 1)/(tan(cutoff*pi/rate) + 1)
            filt = (z**-1 + c)/(1 + c*z**-1)
            return filt(signal)
        dic = {u"Frquência de 'Corte' (Hz)":(700,int,(0,20000))}
        inst = Filtro(all_pass, dic, u"Passa Tudo")
        inst.vparams[0] = cutoff
        return inst
        
    @staticmethod
    def limitador(threshold=.5):
        """ Filtro limitador. Limita as amplitudes ao limiar
        """
        def the_limiter(sig,threshold):
            sig = thub(sig, 2)
            size=256
            env=envelope.rms
            cutoff=pi/2048
            return sig * Stream( 1. if el <= threshold else threshold / el
                   for el in maverage(size)(env(sig, cutoff=cutoff)) )

        dic = {u"Limiar":(.5,float,(0,1))}
        inst = Filtro(the_limiter, dic, u"Limitador")
        inst.vparams[0] = threshold
        return inst
    
    
    @staticmethod
    def compressor(threshold=.5, slope=.5):
        """ Atenua os sons a partir de certo limiar com uma tangente
        """
        def compressor(sig,threshold,slope):
            sig = thub(sig, 2)
            size=256
            env=envelope.rms
            cutoff=pi/2048
            return sig * Stream(1. if el <= threshold else (slope + threshold*(1 - slope)/el)
                    for el in maverage(size)(env(sig, cutoff=cutoff)) )

        dic = {u"Limiar":(.5,float,(0,1)),
               u"Tangente":(.5,float,(0,1))}
        inst = Filtro(compressor, dic, u"Compressor")
        inst.vparams[0] = threshold
        inst.vparams[1] = slope
        return inst
        
    @staticmethod
    def dist_wire(threshold=.5):
        """ Distorção Wire
        """
        @tostream
        def distwire(sig,threshold):
            for el in sig:
                if builtins.abs(el) < threshold: yield el
                else: yield el/builtins.abs(el) - el

        dic = {u"Limiar":(.5,float,(0,1))}
        inst = Filtro(distwire, dic, u"Distwire")
        inst.vparams[0] = threshold
        return inst
    
   
    filtros = {u"Filtros Básicos": (passa_altas,passa_baixas,passa_tudo)
            , u"Limitadores": (limitador,compressor)
    
                , u"Distorções": (dist_wire,)
                , u"Delays": (eco,)                
                }
        
        



#filtro1 = Filtro.eco()
#eco = Filtro.Eco()
"""
tocar = AudioIO()
entrada = tocar.record()
saida = eco.out(entrada)
tocar.play(saida)
stop = raw_input("Pressione ENTER para parar o áudio")
tocar.close()
"""


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







  
def the_resonator (signal,freq,band):
    res = resonator(freq*Hz,band*Hz)
    return res(signal)
    

"""
Atenua as partes abaixo de certo limite
"""
def expander(sig,threshold,slope):
      sig = thub(sig, 2)
      size=256
      env=envelope.rms
      cutoff=pi/2048
      return sig * Stream(slope if el <= threshold else 0
                      for el in maverage(size)(env(sig, cutoff=cutoff)) )

"""
Atenua partes do sinal maior do que certo limite
"""



def phaser (sig, cutoff):
   # sig = thub(sig/2, 2)
    #func = (lambda sig: all_pass(sig,cutoff*Hz))
    return CascadeFilter(lambda signal: all_pass(signal,cutoff*(6+5*sinusoid(2*Hz))*Hz ) for param in xrange(7,8))(sig)
  #  return sig + all_pass(all_pass(all_pass(all_pass(sig,cutoff*1.2*Hz),cutoff*0.8*Hz),cutoff*1.05*Hz),cutoff*Hz)

def teste (samplefreq=44100):
      return (pi*samplefreq)/((pi*samplefreq)*2 + z**2)
            
def distortion1 (sig):
    gen = 10 + 5*sinusoid(5*Hz)    
    return atan(sig*gen)/(pi/2)

#Flanger -> Sinal + sinal c/ delay variante
def flanger (sig):
    variante = line(10.0*s,10.0*s/1000.0,30.0*s/1000.0)
    sig = thub(sig, 2)
    return sig 


"""digital_filters = {"lowpass": ["Passa-baixas",low_pass,("Frequência de Corte (Hz)"),(500)]
, "highpass": ["Passa-altas",high_pass,("Frequência de Corte (Hz)"),(800)]
, "ressonator": ["Ressonador",th  sig = thub(sig, 2)e_resonator,("Frequência Ressonante (Hz)","Tamanho da Banda (Hz)"),(800,100)]
, "limiter": ["Limitador",the_limiter,("Início (0-1)"),(0.5) ]
, "echo": ["Eco",echo,("Tempo de Eco (s)"),(0.05) ]
, "expander": ["Expansor",expander,("Fim (0-1), Fator (0-1)"),(0.5,0.001) ]
, "compressor": ["Compressor",compressor,("Início (0-1), Fator (0-1)"),(0.5,0.001) ]

    }
"""


""" #Teste de sexta
vabs = builtins.abs
@tostream
def distwire(sig):
    for el in sig:
        if vabs(el) < .5: yield el
        else: yield el/vabs(el) - el

with AudioIO(True) as saida:
    data = sinusoid(440*Hz)
    output = phaser(distwire(data),400) 
    saida.play(output)


"""

