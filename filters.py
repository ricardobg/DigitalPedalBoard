# -*- coding: utf-8 -*-
"""
Arquivo para guardar os filtros criados.
Todo filtro é uma instância da classe Filtro, que além
da função que trata o sinal, contém outras informações,
como parâmetros, nome, uso do pedal de expressão.
"""
from audiolazy import *
rate = 44100
s,Hz = sHz(rate)
#chunks.size = 16


@tostream
def envoltoria(sig,alpha=.9999):
    last = 0.    
    for el in sig:
        if el < last: 
            last *= alpha
            yield last
        else:
            last = el
            yield last



"""
Funções que retornam Stream seguidas pela função que instancia o seu filtro com
seus parâmetros, nome, etc.
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
    Retorna uma instância do Eco
    """
    dic = {u"Intervalo (s)":(0.2,float,(0,5))}
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
    Flanger
    """
    dic = {u"Frequência (mHz)":(.3,float,(.01,5))
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
    Delay variável com o pedal
    """
    dic = {u"Lag (ms)":(2.,float,(1,50))}
    inst = Filtro(delay_variavel, dic, u"Variable Echo",True)
    inst.vparams[0] = lag
    return inst
    

# FILTROS BÁSICOS

@tostream
def amp(sig, ganho, ganho_max):
     for el in sig:
         ret = el*(next(iter(ganho))*ganho_max)            
         if builtins.abs(ret) > 1: yield el/builtins.abs(el)
         else: yield ret
def amplificador(ganho_max=5.0):
    """
    Filtro que amplifica o sinal (ganho>1)
    """    
    dic = {u"Valor máximo da Amplificação":(5.0,float,(0.1,10))}
    inst = Filtro(amp, dic, u"Amplifier", True)
    inst.vparams[0] = ganho_max
    return inst
    
def low_pass (signal, cutoff):
        filt = lowpass(cutoff/(float(cutoff)))
        return filt(signal)
def passa_baixas(cutoff=700):
    """ 
    Filtro que atenua altas frequências
    """
    dic = {u"Frquência de Corte (Hz)":(700,int,(0,20000))}
    inst = Filtro(low_pass, dic, u"Low Pass")
    inst.vparams[0] = cutoff
    return inst


def high_pass (signal,cutoff):
        filt = highpass(cutoff*Hz)
        return filt(signal)
def passa_altas(cutoff=700):
    """  
    Filtro que atenua baixas frequências
    """
    dic = {u"Frquência de Corte (Hz)":(700,int,(0,20000))}
    inst = Filtro(high_pass, dic, u"High Pass")
    inst.vparams[0] = cutoff
    return inst
    
def all_pass (signal, cutoff):
        c = (tan(cutoff*pi/rate) - 1)/(tan(cutoff*pi/rate) + 1)
        filt = (z**-1 + c)/(1 + c*z**-1)
        return filt(signal)
def passa_tudo(cutoff=700):
    """ 
    Filtro que não muda a intensidade, apenas a fase da sua entrada
    """
   
    dic = {u"Frquência de 'Corte' (Hz)":(700,int,(0,20000))}
    inst = Filtro(all_pass, dic, u"All Pass")
    inst.vparams[0] = cutoff
    return inst
    
    
    
# LIMITADORES
    
def the_limiter(sig,threshold):
        sig = thub(sig, 2)
        return sig * Stream( 1. if el <= threshold else threshold / el
               for el in envoltoria(sig) )

def limitador(threshold=.5):
    """ 
    Filtro limitador. Limita as amplitudes ao limiar
    """
    dic = {u"Limiar":(.5,float,(0,1))}
    inst = Filtro(the_limiter, dic, u"Limiter")
    inst.vparams[0] = threshold
    return inst

def the_compressor(sig,threshold,slope):
        sig = thub(sig, 2)
        return sig * Stream(1. if el <= threshold else (slope + threshold*(1 - slope)/el)
                for el in envoltoria(sig))
def compressor(threshold=.5, slope=.5):
    """ 
    Atenua os sons a partir de certo limiar com uma tangente
    """
    dic = {u"Limiar":(.5,float,(0,1)),
           u"Tangente":(.5,float,(0,1))}
    inst = Filtro(the_compressor, dic, u"Compressor")
    inst.vparams[0] = threshold
    inst.vparams[1] = slope
    return inst

def expander(sig,threshold,slope):
      sig = thub(sig, 2)
      return sig * Stream((slope + threshold*(1 - slope)/el) if (el <= threshold and el > 0) else 1.
                      for el in envoltoria(sig))

def filtro_expander(threshold=.5, slope=.5):
    """ 
    Atenua os sons a abaixo de certo limiar com uma tangente
    """
    dic = {u"Limiar":(.5,float,(0,1)),
           u"Tangente":(.5,float,(0,1))}
    inst = Filtro(expander, dic, u"Expander")
    inst.vparams[0] = threshold
    inst.vparams[1] = slope
    return inst
# DISTORÇÕES
  
@tostream
def distwire(sig,threshold):
    for el in sig:
        if builtins.abs(el) < threshold: yield el
        else: yield el/builtins.abs(el) - el
def dist_wire(threshold=.5):
    """ Distorção Wire
    """
    dic = {u"Limiar":(.5,float,(0,1))}
    inst = Filtro(distwire, dic, u"Distwire")
    inst.vparams[0] = threshold
    return inst

def senoide(sig,freq):
    return sig*sinusoid(freq*Hz)    
def filtro_senoide(freq=700):
    """ 
    Multiplica por senóide
    """
    dic = {u"Frequência (Hz)":(700,float,(0,20000))}
    inst = Filtro(senoide, dic, u"Sinusoid")
    inst.vparams[0] = freq
    return inst

def senoide_var(sig,freq,freq_max):
    return sig*sinusoid(freq*freq_max*Hz)    
def filtro_senoide_var(freq_max=10000):
    """ 
    Multiplica por senóide variável
    """
    dic = {u"Frequência Máxima (Hz)":(10000,float,(0,20000))}
    inst = Filtro(senoide_var, dic, u"Ring modulation",True)
    return inst

@tostream
def corta_var(sig, corta, limite):
    for el,v in izip(sig,corta):
        if v > limite: yield 0.
        else: yield el
def filtro_corta(limite=.5):
    """ 
    Corta o som
    """
    dic = {u"Limite":(.5,float,(0,1))}
    inst = Filtro(corta_var, dic, u"Cut",True)
    return inst


def mult_env(sig,alpha):
    return sig * envoltoria(sig,alpha)

def filtro_mult_env(alpha=.9999):
    """ 
    Corta o som
    """
    dic = {u"Alpha":(.9999,float,(0.1,.999999))}
    inst = Filtro(mult_env, dic, u"Envelop",False)
    return inst

def the_resonator (signal,freq,band):
    res = resonator(freq*Hz,band*Hz)
    return res(signal)
    
def filtro_res(freq=900,band=5):
    """
    Ressonador
    """
    dic = {u"Frequência":(900,float,(0,20000))
    , u"Banda": (5,float,(1,100))}
    inst = Filtro(the_resonator, dic, u"Resonator",False)
    return inst
    
# Variável ControlStream (ou inteiro) com a entrada do pedal
pedal = ControlStream(0.1)
     
class Filtro:
    """ 
    Classe para os filtros
    params: Contém o dicionário que caracteriza o filtro
    vparams: Valores padrão dos parâmetros
    name: nome do filtro
    usa_pedal: Indica se o filtro usa ou não o valor do pedal de expressão
      
    """
    def __init__(self, fun, dic, name, usa_pedal=False):
        """        
        fun: Uma função que recebe um Stream e retorna outro Stream (além de outros parametros)
        dic: Dicionário que dá um nome para cada parametro do filtro e 
        o seu valor é uma tupla que contém (valor_padrao, tipo, (valor_inicial,valor_final))
         é uma tupla com os valores dos parâmetros
        
        A variável estatica filtros contém um dicionário definido pelo grupo de filtros e por uma tupla contendo
        as funções que instanciam os filtros
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
        