from hpprime import eval

lt = 0
dt = 1

def init():
  global lt,dt
  lt = int(eval('ticks'))
  dt = 1

def update():
  global lt,dt
  t=int(eval('ticks'))
  dt=t-lt
  lt=t

def get_fps():
  return 1000/dt

def get_frame_elapsed():
  return int(eval('ticks')) - lt