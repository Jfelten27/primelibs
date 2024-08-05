from sys import *
path.append('.')
path.append('../spellcheck.hpappdir')

import spellcheckmain as sp

def check(word):
  return sp.check(word)