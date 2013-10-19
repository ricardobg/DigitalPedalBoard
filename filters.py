from audiolazy import *

"""
allpass,lowpass,highpass:
G(z) = (b0 + b1*z**-1) / (1 + a1*z**-1)
K = tg (pi*fc/fs)
"""


"""
b0 = K/(K + 1)
b1 = k/(K+1)
a1 = (K-1)/(K+1)
"""
def low_pass (cutoff):
    k = tan(pi*cutoff)
    b0 = k/(k + 1)
    b1 = k/(k + 1)
    a1 = (k - 1)/(k + 1)
    filt = (b0 + b1*z**-1) / (1 + a1*z**-1)
    return filt

def highpass (cutoff):
    pass

def all_pass (ars):
    pass



"""
G(z) = (b0 + b1*z**-1 + b2*z**-2) / (1 + a1*z**-1 + a2*z**-2)

"""
def ressonator ():
    pass


"""
G(z) = (b0 + b1*z**-1 + b2*z**-2) / (1 + a1*z**-1 + a2*z**-2)

"""
def limiter ():
    pass

def compressor ():
    pass

def expander():
    pass

def distortion ():
    pass

def phaser ():
    pass

def flanger ():
    pass
