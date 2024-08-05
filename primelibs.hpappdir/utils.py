from math import *
from hpprime import *

def counter(s):
    output = {}
    for c in s:
        try:
            output[c] += 1
        except KeyError:
            output[c] = 1
    return output

def round(n):
  return copysign(int(abs(n) + 0.5), n)

def rgb(*c):
  if len(c) == 1:
    return ((c[0] / 255) >> 16, ((c[0] / 255) >> 8) & 255, (c[0] / 255) & 255)
  if len(c) == 3:
    return (int(255 * c[0]) << 16) | (int(255 * c[1]) << 8) | int(255 * c[2])

def fontSizeNum(n):
  return max(min(floor(round(n) / 2) - 4, 7), 1)

def drawProgressBar(progress, color):
  fillrect(0, 0, 0, int(320 * progress), 14, color, color)

def avg(l):
  return sum(l)/len(l)

def textw(txt,fnt=2):
  dimgrob(9,512,22,0)
  return eval('textout_p("' + txt.replace('\\', '\\\\').replace('"', '\\"') + '",G9,0,0,0,0)')

def texth(fnt):
  return [14,10,12,14,16,18,20,22][fnt]