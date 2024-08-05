from hpprime import *

red = 0
green = 0
blue = 0
bg1 = 0
bg2 = 0
fg = 0

light = {
  'red': 0xffe0d0,
  'green': 0xbdffc8,
  'blue': 0xd0e0ff,
  'bg1': 0xffffff,
  'bg2': 0xc8c8c8,
  'fg': 0x000000,
  'button': 0x808080,
  'sel': 8
}

dark = {
  'red': 0x601008,
  'green': 0x086020,
  'blue': 0x204060,
  'bg1': 0x202020,
  'bg2': 0x383838,
  'fg': 0xfff0e0,
  'button': 0x585858
}

def init(theme):
  global red
  global green
  global blue
  global bg1
  global bg2
  global fg
  global buttoncolor
  red = theme['red']
  green = theme['green']
  blue = theme['blue']
  bg1 = theme['bg1']
  bg2 = theme['bg2']
  fg = theme['fg']
  buttoncolor = theme['button']

if eval('Theme(1)') == 1:
  init(light)
else:
  init(dark)