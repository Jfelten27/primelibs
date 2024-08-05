from hpprime import *

x = -1
y = -1
_x = -1
_y = -1
mtype = 0
dx = 0
dy = 0
down = False
tap = False

def update():
  global x
  global y
  global _x
  global _y
  global mtype
  global dx
  global dy
  global tap
  global down
  c = eval('mouse')[0]
  if len(c):
    c[0]=(c[0]+2**63)%2**64-2**63
    c[1]=(c[1]+2**63)%2**64-2**63
    if c[4] == 0 or not down:
      x = c[0]
      y = c[1]
      _x = c[0]
      _y = c[1]
      down = True
      tap = True
      mtype = c[4]
    elif c[4] == 2 and down:
      x = c[0]
      y = c[1]
      dx = _x - c[0]
      dy = _y - c[1]
      _x = x
      _y = y
      mtype = c[4]
      tap = False
  else:
    dx = 0
    dy = 0
    if down:
      x, y = _x, _y
      down = False
    else:
      x, y = -1, -1
      tap = False

def istapped():
  return tap and not down