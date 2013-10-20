from audiolazy import *
"""
rate - Samples/second
"""
"""
allpass,lowpass,highpass:
G(z) = (b0 + b1*z**-1) / (1 + a1*z**-1)
k = tg (pi*fc/fs)

fs - sample rating
fc - cutoff frequency
"""


"""
b0 = k/(k + 1)
b1 = k/(k+1)
a1 = (k-1)/(k+1)
"""
def low_pass (cutoff,samplingFreq=44100):
    k = tan(pi*cutoff/samplingFreq)
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
