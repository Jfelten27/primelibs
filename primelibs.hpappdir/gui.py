from hpprime import *
from utils import *
from sys import *

from palette import *

import kbd, utils, time, pointer

dimgrob(1,320,240,0)

class Component:
  def __init__(self):
    self.master = None
    self.x = 0
    self.y = 0
    self.w = 0
    self.h = 0
    self.tabbed = False
    self.scrolling = False

  def getPos(self):
    try:
      x,y = self.master.getPos()
      return (x+self.x,y+self.y)
    except AttributeError:
      pass

  def getSize(self):
    return self.w, self.h

  def setPos(self,x,y):
    self.x = x
    self.y = y

  def setSize(self,w,h):
    self.w = w
    self.h = h

  def destroy(self):
    self.master.widgets.remove(self)

  def isPressed(self):
    x, y = self.getPos()
    return x <= pointer.x < x + self.w and y <= pointer.y < y + self.h

  def isTapped(self):
    return pointer.istapped() and self.isPressed()

  def draw(self):
    pass

  def update(self):
    if pointer.istapped() and self.isPressed():
      self.master.settab(self.master.widgets.index(self))
    elif pointer.mtype == 2 and self.isPressed() and not self.scrolling:
      self.scrolling = True
    elif not pointer.down:
      self.scrolling = False
      self.xscroll = self.yscroll = 0
    if self.scrolling:
      self.xscroll = pointer.dx
      self.yscroll = pointer.dy

class Frame(Component):
  def __init__(self):
    super().__init__()
    self.widgets = []
    self.tabindex = 0
    self.switch = ''
    self.ret = ''
    self.prevwin = ''
    self.type = ''

  def switchview(self, v, r=''):
    self.switch = v
    self.ret = r

  def add(self,widget):
    self.widgets.append(widget)
    widget.master = self

  def update(self):
    if kbd.testkey('tab') or (kbd.testkey('right') and not isinstance(self.widgets[self.tabindex], TextField)):
      self.movetab(1)
      if isinstance(self.widgets[self.tabindex], Titlebar):
        self.movetab(1)
    elif kbd.testkey('+tab') or (kbd.testkey('left') and not isinstance(self.widgets[self.tabindex], TextField)):
      self.movetab(-1)
      if isinstance(self.widgets[self.tabindex], Titlebar):
        self.movetab(-1)
    for w in self.widgets:
      w.update()
    if not self.switch:
      self.ret = ''
      self.prevwin = ''

  def draw(self):
    for w in self.widgets:
      w.draw()

  def settab(self, v):
    self.widgets[self.tabindex].tabbed = False
    self.tabindex = v
    self.tabindex %= len(self.widgets)
    self.widgets[self.tabindex].tabbed = True

  def movetab(self, v):
    self.settab(self.tabindex + v)

  def getPos(self):
    return self.x, self.y

class Window(Frame):
  def __init__(self):
    super().__init__()
    self.titlebar = Titlebar()
    self.add(self.titlebar)
    self.setTitle('PrimeGUI Window')
    self.closebutton = CloseButton()
    self.add(self.closebutton)
    self.setPos(80,60)
    self.setSize(160,120)
    self.isRunning = True

  def setSize(self, w, h):
    super().setSize(w, h)
    self.titlebar.setSize(self.w, 20)

  def setTitle(self,t):
    self.title = t
    self.titlebar.setText(self.title)

  def getPos(self):
    return self.x, self.y

  def close(self):
    self.isRunning = False

  def update(self):
    super().update()
    kbd.update()
    pointer.update()
    time.update()

  def draw(self):
    fillrect(1,self.x,self.y,self.w,self.h,fg,bg2)
    fillrect(1,self.x,self.y,self.w,20,bg2,bg2)
    super().draw()

  def mainloop(self):
    kbd.init()
    time.init()
    kbd.update()
    while self.isRunning:
      self.update()
      self.draw()
      blit(0,0,0,1)

class TextBox(Component):
  def __init__(self):
    super().__init__()
    self.text = 'e'
    self.txtcolor = fg
    self.font = 3
    self.padx = 3
    self.pady = 2
    self.fixedWidth = False

  def setText(self,t):
    self.text = t
    self.updateText()

  def setFont(self,f):
    self.font = f
    self.updateText()

  def setPadding(self,x,y):
    self.padx = x
    self.pady = y

  def updateText(self):
    self.lines = []
    if self.fixedWidth:
      lines = [l.split()[::-1] for l in self.text.split('\n')][1:]
      line = ''
      for l in lines:
        while l:
          word = l.pop()
          if textw(line+word,self.font)<=self.w-2*self.padx:
            line += word
          else:
            self.lines.append(line)
            line = word
        self.lines.append(line)
        line = ''
        print(lines)
    else:
      self.lines = self.text.split('\n')

  def setFixedWidth(self,fw):
    self.fixedWidth = fw
    self.updateText()

  def update(self):
    super().update()
    w = 2*self.padx+textw(self.text,self.font)
    h = 2*self.pady+texth(self.font)
    self.setSize(w,h)

  def draw(self):
    x,y = self.getPos()
    for i,line in enumerate(self.lines):
      if self.font == 0:
        textout(1, x + self.padx, y + self.pady + i * texth(self.font), line, self.txtcolor)
      else:
        eval('textout_p("{0}",G1,{1},{2},{3},{4})'.format(line,x+self.padx,y+self.pady+i*texth(self.font),self.font,self.txtcolor))

class Button(Component):
  def __init__(self):
    super().__init__()
    self.wasPressed = False
    self.color = buttoncolor

  def onPress(self):
    pass

  def onRelease(self):
    pass

  def setOnPress(self,f):
    self.onPress = f

  def setOnRelease(self,f):
    self.onRelease = f

  def setColor(self,c):
    self.color = c

  def draw0(self):
    x,y = self.getPos()
    w,h = self.getSize()
    color = int((blue + self.color)/2) if self.tabbed else self.color
    lightcolor = sum([int(avg(2*[v>>(16-8*i)]+[0xff]))<<(16-8*i) for i,v in enumerate([color&(0xff<<(16-8*i)) for i in range(3)])])
    fillrect(1,x,y,w,h,color,lightcolor)

  def draw(self):
    x,y = self.getPos()
    w,h = self.getSize()
    self.draw0()
    if self.wasPressed:
      eval('RECT_P(G1,{0},{1},{2},{3},#80FFFFFF)'.format(x,y,x+w-1,y+h-1))

  def update(self):
    x, y = self.getPos()
    w, h = self.getSize()
    if pointer.istapped() and self.isPressed() or (self.tabbed and kbd.testkey('enter')):
      self.onPress()
      self.wasPressed = True

    if self.wasPressed and not self.isPressed():
      self.onRelease()
      self.wasPressed = False

class CloseButton(Button):
  def __init__(self):
    super().__init__()
    self.setSize(20,20)
    self.color = red

  def onRelease(self):
    self.master.close()

  def draw0(self):
    super().draw0()
    x,y = self.getPos()
    w,h = self.getSize()
    margin = 5
    for i in range(-1,2):
      for j in range(-1,2):
        line(1,x+margin+i,y+margin+j,x+w-margin-1+i,y+h-margin-1+j,self.color)
        line(1,x+w-margin-1+i,y+margin+j,x+margin+i,y+h-margin-1+j,self.color)

  def update(self):
    x, y = self.master.getPos()
    w, h = self.master.getSize()
    self.setPos(w-20,0)
    if kbd.testkey('esc'):
      self.onRelease()
    if self.tabbed:
      self.master.movetab(1)
    super().update()


class TextButton(Button,TextBox):
  def __init__(self):
    super().__init__()
    TextBox.__init__(self)
    self.text = ''
    self.lines = []
    self.txtcolor = fg
    self.font = 3
    self.padx = 3
    self.pady = 2

  def update(self):
    super().update()
    w = 2*self.padx+textw(self.text,self.font)
    h = 2*self.pady+len(self.lines)*texth(self.font)
    self.setSize(w,h)

  def draw0(self):
    super().draw0()
    x,y = self.getPos()
    TextBox.draw(self)

class Titlebar(TextBox):
  def __init__(self):
    super().__init__()
    self.setFont(0)
    self.setSize(320, 14)

  def update(self):
    print(self.getPos(), pointer.x, pointer.y)
    Component.update(self)
    self.setSize(self.master.w, self.h)
    print(self.getPos(), pointer.x, pointer.y)
    if self.isPressed():
      self.master.x += pointer.dx
      self.master.y += pointer.dy
      print(e)

  def draw(self):
    x, y = self.getPos()
    fillrect(1, x, y, self.master.w, self.h, bg1, bg1)
    line(1, x, y + self.h, x + self.master.w - 1, y + self.h, fg)
    super().draw()

  def update(self):
    if self.tabbed:
      self.master.movetab(1)

class TextField(Component):
  def __init__(self):
    super().__init__()
    self.label = ''
    self.text = ''
    self.cursor = Pointer()
    self.h = 15
    self.subtype = 'text'

  def type(self, c):
    if c == '':
      return
    elif c == 'left':
      if self.cursor.char > 0:
        self.movecursor(-1)
    elif c == 'right':
      if self.cursor.char < len(self.text):
        self.movecursor(1)
    elif c == 'backspace':
      if self.cursor.char > 0:
        self.text = self.text[:self.cursor.char - 1] + self.text[self.cursor.char:]
        self.movecursor(-1)
    elif c == 'delete':
      if self.cursor.char < len(self.text):
        self.movecursor(1)
        self.type('backspace')
        return
    elif c == 'enter':
      self.enter()
    elif c == 'tab':
      pass
    else:
      self.text = self.text[:self.cursor.char] + c + self.text[self.cursor.char:]
      self.movecursor(len(c))
    self.cursor.time = 0

  def updatecursor(self):
    self.cursor.x = utils.textw(self.text[:self.cursor.char])

  def movecursor(self, v):
    self.cursor.char += v
    self.updatecursor()

  def draw(self):
    x, y = self.getPos()
    textout(1, x, y + 1, self.label, fg)
    _x = utils.textw(self.label)
    fillrect(1, x + _x, y, self.w - _x - 1, 15, fg, bg1)
    eval('textout_p("{}", G1, {}, {}, 0, {}, {})'.format(self.text, x + _x + 1, y + 1, fg, self.w - _x - 2))
    if self.tabbed:
      if (self.cursor.time % 1000) < 500:
        line(1, x + _x + 1 + self.cursor.x, y + 1, x + _x + 1 + self.cursor.x, y + 14, fg)

  def update(self):
    super().update()
    if self.tabbed:
      self.cursor.time += time.dt
      if self.subtype == 'text':
        self.type(kbd.getkey())
      elif self.subtype == 'num':
        try:
          self.type({'"': '0', 'y': '1', 'z': '2', '#': '3', 'u': '4', 'v': '5', 'w': '6', 'q': '7', 'r': '8', 's': '9'}[kbd.getkey()])
        except KeyError:
          self.type(kbd.getkey())
      self.type(kbd.ugetkey())
    else:
      self.cursor.char = 0
      self.updatecursor()

  def setText(self, t):
    self.text = t

  def setLabel(self, l):
    self.label = l

  def enter(self):
    pass

class Pointer():
  def __init__(self, line=0, word=0, char=0):
    self.time = 0
    self.char = char
    self.x = 0
    self.y = 0
    self.prevx = 0

  def __eq__(p1, p2):
    return p1.line == p2.line and p1.word == p2.word and p1.char == p2.char

  def __str__(self):
    return str((self.line, self.word, self.char))

class InfoBar(Component):
  def __init__(self):
    super().__init__()
    self.setSize(320, 14)
    self.text = ''

  def draw(self):
    fillrect(1, 0, 240 - self.h, self.w, self.h, bg1, bg1)
    line(1, 0, 240 - self.h, 320, 240 - self.h, fg)
    textout(1, 1, 241 - self.h, self.text, fg)

  def update(self):
    if self.tabbed:
      self.master.movetab(1)

  def setText(self, t):
    self.text = t