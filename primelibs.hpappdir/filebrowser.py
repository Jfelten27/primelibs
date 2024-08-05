from math import *
from hpprime import *
from palette import *

import gui, kbd, utils, pointer

class CancelButton(gui.TextButton):
  def __init__(self):
    super().__init__()
    self.setPos(234, 217)
    self.setSize(35, 20)
    self.setText('Cancel')
    self.setFont(0)

  def update(self):
    super().update()
    if kbd.getkey() == 'esc' or kbd.ugetkey() == 'esc':
      self.onRelease()

  def onRelease(self):
    self.master.close(0)

class SelectButton(gui.TextButton):
  def __init__(self):
    super().__init__()
    self.setPos(282, 217)
    self.setSize(35, 20)
    self.setFont(0)

  def onRelease(self):
    self.master.filename.enter()

class SaveButton(SelectButton):
  def __init__(self):
    super().__init__()
    self.setText('Save')

class OpenButton(SelectButton):
  def __init__(self):
    super().__init__()
    self.setText('Open')

class ExportButton(SelectButton):
  def __init__(self):
    super().__init__()
    self.setText('Export')
    self.setPos(277, 217)

class NameField(gui.TextField):
  def __init__(self, ext=''):
    super().__init__()
    self.setText(ext)
    self.setLabel('Name: ')
    self.setPos(111, 199)
    self.setSize(209, 15)

  def draw(self):
    x, y = self.getPos()
    fillrect(1, x, y, self.w, 240 - y, bg1, bg1)
    super().draw()

  def enter(self):
    if self.text:
      self.master.close('../' + eval('Apps')[self.master.sidebar.selection - 1] + '.hpappdir/' + self.text)
    else:
      self.master.settab(2)

class Sidebar(gui.Component):
  def __init__(self):
    super().__init__()
    self.x = 0
    self.y = 15
    self.w = 111
    self.h = 225
    self.offset = 0
    self.selection = 1
    self._draw = True

  def draw(self):
    if not (self._draw or self.tabbed):
      return
    line(1,110,self.y,110,240,fg)
    li=eval('Apps')
    top = self.offset // 14
    #print(top)
    for i, a in enumerate(li[top:top + ceil(self.h / 14)]):
      color=(blue if self.tabbed else bg2)
      if top + i==self.selection-1:
        fillrect(1,0,14 * (top + i) - self.offset + self.y,110,14,color,color)
      else:
        fillrect(1,0,14 * (top + i) - self.offset + self.y,110,14,bg1,bg1)
      if eval('TEXTOUT_P("'+str(a)+'",G1,1,'+str(14 * (top + i) - self.offset + self.y)+'+1,2,'+str(fg)+',110)')>110:
        eval('TEXTOUT_P("...",G1,100,'+str(14 * (top + i) - self.offset + self.y)+'+1,2,'+str(fg)+',10,'+str(bg1)+')')
    #fillrect(1, 111, self.y, 210, 240, 0xffffff, 0xffffff)
    self._draw = self.tabbed

  def update(self):
    super().update()
    if self.scrolling:
      self.offset = max(min(self.offset + pointer.dy, 14 * len(eval('Apps')) - self.h), 0)
      self._draw = True
    if self.isTapped():
      self.selection = (pointer.y + self.offset - self.getPos()[1]) // 14 + 1
    if self.tabbed:
      if kbd.testkey('up'):
        self.selection = max(self.selection - 1, 1)
        self.offset = min(self.offset, 14 * self.selection - 14)
        self.master.filelist.updated = False
      elif kbd.testkey('down'):
        self.selection = min(self.selection + 1, len(eval('Apps')))
        self.offset = max(self.offset, 14 * self.selection - self.h)
        self.master.filelist.updated = False
    self.master.appname = eval('Apps')[self.selection - 1]

class FileList(gui.Component):
  def __init__(self):
    super().__init__()
    self.setPos(111, 15)
    self.setSize(209, 184)
    self.offset = 0
    self.selection = 1
    self.fileslist = []
    self._draw = True
    self.updated = False
    self.search = ''

  def updatefiles(self):
    if self.updated:
      return
    self.fileslist = eval('EXPR(REPLACE("'+self.master.appname+'"+".AFiles()"," ","_"))')
    i = 0
    while i < len(self.fileslist):
      f = self.fileslist[i]
      if not f.endswith(self.master.extfilter):
        try:
          self.fileslist.remove(f)
          i -= 1
        except:
          pass
      i += 1
    try:
      self.fileslist.sort()
    except:
      pass
    self.updated = True
    self._draw = True

  def find(self, query):
    for i, f in enumerate(self.fileslist):
      if f.startswith(query):
        self.selection = i + 1
        return True
    return False

  def correctPosition(self):
    self.offset = min(self.offset, 14 * (self.selection - 1))
    self.offset = max(self.offset, 14 * self.selection - self.h)

  def draw(self):
    #super().draw()
    if not (self._draw or self.tabbed):
      return
    fillrect(1, self.x, self.y, self.w, self.h, bg1, bg1)
    li=self.fileslist
    if li==[]:
      eval('TEXTOUT_P("This app has no files.",G1,150,20,1,#A0A0A0)')
    else:
      for i, f in enumerate(li[self.offset // 14: (self.offset + self.h) // 14 + 1]):
        if i + self.offset // 14 == self.selection-1 :
          color = blue if self.tabbed else bg2
          fillrect(1,111,14 * i - self.offset % 14 + self.y, 210, 14, color, color)
        else:
          fillrect(1,111,14 * i - self.offset % 14 + self.y, 210, 14, bg1, bg1)
        textout(1, 120, 14 * i - self.offset % 14 + self.y, str(f), fg)
    self._draw = self.tabbed

  def update(self):
    super().update()
    if self.scrolling:
      self.offset = max(min(self.offset + pointer.dy, 14 * len(self.fileslist) - self.h), 0)
      self._draw = True
    if self.isTapped():
      self.selection = (pointer.y + self.offset - self.getPos()[1]) // 14 + 1
    if not self.tabbed:
      self.updatefiles()
      return
    if len(self.fileslist) == 0:
      return
    elif kbd.testkey('up'):
      self.selection = (self.selection - 2) % len(self.fileslist) + 1
      self.offset = min(self.offset, 14 * (self.selection - 1))
    elif kbd.testkey('down'):
      self.selection = self.selection % len(self.fileslist) + 1
      self.offset = max(self.offset, 14 * self.selection - self.h)
    elif kbd.testkey('enter'):
      self.master.filename.enter()
    else:
      self.search += kbd.getkey()
      self.search += kbd.ugetkey()
      if kbd.getkey() or kbd.ugetkey():
        self.find(self.search)
        self.correctPosition()
    if len(self.fileslist):
      self.master.filename.setText(self.fileslist[self.selection - 1])

class FileBrowser(gui.Frame):
  def __init__(self, ext=''):
    super().__init__()
    self.setSize(320, 240)
    dimgrob(1, 320, 240, bg2)
    self.sidebar = Sidebar()
    self.add(self.sidebar)
    self.filelist = FileList()
    self.add(self.filelist)
    self.appname = eval('Apps')[self.sidebar.selection - 1]
    self.extfilter = ext

  def update(self):
    self.filelist.updatefiles()
    if self.prevwin:
      self.switchto = self.prevwin
    super().update()

  def close(self, ret):
    self.switchview(self.switchto, ret)

class Save(FileBrowser):
  def __init__(self, ext=''):
    super().__init__(ext)
    self.type = 'save'
    self.filename = NameField(self.extfilter)
    self.add(self.filename)
    self.cancelbutton = CancelButton()
    self.add(self.cancelbutton)
    self.savebutton = SaveButton()
    self.add(self.savebutton)
    self.titlebar = gui.Titlebar()
    self.titlebar.setText('Save...')
    self.add(self.titlebar)
    self.settab(2)
    self.filelist.updatefiles()

class Open(FileBrowser):
  def __init__(self, ext=''):
    super().__init__(ext)
    self.type = 'open'
    self.filename = NameField()
    self.add(self.filename)
    self.cancelbutton = CancelButton()
    self.add(self.cancelbutton)
    self.openbutton = OpenButton()
    self.add(self.openbutton)
    self.titlebar = gui.Titlebar()
    self.titlebar.setText('Open...')
    self.add(self.titlebar)
    self.settab(1)
    self.filelist.updatefiles()

class Export(FileBrowser):
  def __init__(self, ext=''):
    super().__init__(ext)
    self.type = 'export'
    self.extfilter = ext
    self.filename = NameField()
    self.add(self.filename)
    self.cancelbutton = CancelButton()
    self.cancelbutton.setPos(229, 217)
    self.add(self.cancelbutton)
    self.exportbutton = ExportButton()
    self.add(self.exportbutton)
    self.titlebar = gui.Titlebar()
    self.titlebar.setText('Export PDF...')
    self.add(self.titlebar)
    self.settab(2)
    self.filelist.updatefiles()

  def update(self):
    if self.ret:
      self.filename.setText(self.ret + self.extfilter)
      self.filename.movecursor(len(self.ret))
    super().update()