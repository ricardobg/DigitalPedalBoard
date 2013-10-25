# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:44:32 2013

@author: Ricardo
"""

from audiolazy import *
rate = 44100
s, Hz = sHz(rate)
sig = karplus_strong(640*Hz).limit(3*s)*.5
smix = Streamix()
smix.add(0, sig.copy())
smix.add(.2*s,sig)
with AudioIO(True) as player:
    player.play(smix, rate=rate)
    