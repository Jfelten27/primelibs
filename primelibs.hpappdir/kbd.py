from hpprime import *

import time

chars = {
          -1: '',
          0: 'f1',
          1: 'f4',
          2: 'up',
          3: 'f7',
          4: 'esc',
          5: 'f2',
          6: 'f5',
          7: 'left',
          8: 'right',
          9: 'f8',
          10: 'f3',
          11: 'f6',
          12: 'f9',
          12: 'down',
          14: 'a',
          15: 'b',
          16: 'c',
          17: 'd',
          18: 'e',
          19: 'backspace',
          20: 'f',
          21: 'g',
          22: 'h',
          23: 'i',
          24: 'j',
          25: 'k',
          26: 'l',
          27: 'm',
          28: 'n',
          29: 'o',
          30: 'enter',
          31: 'p',
          32: 'q',
          33: 'r',
          34: 's',
          35: 't',
          36: '',
          37: 'u',
          38: 'v',
          39: 'w',
          40: 'x',
          41: '',
          42: 'y',
          43: 'z',
          44: '#',
          45: ':',
          47: '\'',
          48: '.',
          49: ' ',
          50: ';'
        }

alphachars = {
          -1: '',
          2: '+up',
          6: 'f5',
          7: '+left',
          8: '+right',
          11: 'f6',
          12: '+down',
          14: 'A',
          15: 'B',
          16: 'C',
          17: 'D',
          18: 'E',
          19: 'backspace',
          20: 'F',
          21: 'G',
          22: 'H',
          23: 'I',
          24: 'J',
          25: 'K',
          26: 'L',
          27: 'M',
          28: 'N',
          29: 'O',
          30: 'enter',
          31: 'P',
          32: 'Q',
          33: 'R',
          34: 'S',
          35: 'T',
          36: '',
          37: 'U',
          38: 'V',
          39: 'W',
          40: 'X',
          41: '',
          42: 'Y',
          43: 'Z',
          45: '-',
          47: '"',
          48: ',',
          49: ' '
        }

shiftchars = {
          -1: '',
          2: '+home',
          6: 'f5',
          7: 'left',
          8: 'right',
          10: 'f12',
          12: '+end',
          14: '^a',
          15: '^b',
          16: '^c',
          17: '^d',
          18: '^e',
          19: '^backspace',
          20: '^f',
          21: '^g',
          22: '^h',
          23: '^i',
          24: '^j',
          25: '^k',
          26: '^l',
          27: '^m',
          28: '^n',
          29: '^o',
          30: 'enter',
          31: '^p',
          32: '^q',
          33: '^r',
          34: '^s',
          35: '^t',
          36: '',
          37: '^u',
          38: '^v',
          39: '^w',
          40: '^x',
          41: '',
          42: '^y',
          43: '^z',
          45: '^-',
          49: 'tab',
          50: '^='
        }

shiftalphachars = {
          -1: '',
          2: 'up',
          4: 'esc',
          6: 'f5',
          7: 'left',
          8: 'right',
          12: 'down',
          14: 'a',
          15: 'b',
          16: 'c',
          17: 'd',
          18: '^+e',
          19: 'backspace',
          20: 'f',
          21: 'g',
          22: 'h',
          23: 'i',
          24: 'j',
          25: 'k',
          26: 'l',
          27: 'm',
          28: 'n',
          29: 'o',
          30: 'enter',
          31: 'p',
          32: '7',
          33: '8',
          34: '9',
          35: '/',
          36: '',
          37: '4',
          38: '5',
          39: '6',
          40: '*',
          41: '',
          42: '1',
          43: '2',
          44: '3',
          45: '-',
          47: '0',
          49: '+tab',
          50: '+'
        }

uchars = {
           0: '',
           30: '1',
           31: '2',
           32: '3',
           33: '4',
           34: '5',
           35: '6',
           36: '7',
           37: '8',
           38: '9',
           39: '0',
           40: 'enter',
           41: 'esc',
           42: 'backspace',
           43: 'tab',
           44: ' ',
           45: '-',
           46: '=',
           47: '[',
           48: ']',
           49: '\\',
           50: '\\',
           51: ';',
           52: '\'',
           53: '`',
           54: ',',
           55: '.',
           56: '/',
           57: 'caps',
           58: 'f1',
           59: 'f2',
           60: 'f3',
           61: 'f4',
           62: 'f5',
           63: 'f6',
           64: 'f7',
           65: 'f8',
           66: 'f9',
           67: 'f10',
           68: 'f11',
           69: 'f12',
           74: 'home',
           75: 'pgup',
           76: 'delete', 
           77: 'end',
           78: 'pgdn',
           79: 'right',
           80: 'left',
           81: 'down',
           82: 'up'
         }

uctrlchars = {
           0: '',
           30: '1',
           31: '2',
           32: '3',
           33: '4',
           34: '5',
           35: '6',
           36: '7',
           37: '8',
           38: '^9',
           39: '^0',
           40: 'enter',
           42: 'backspace',
           44: ' ',
           45: '^-',
           46: '^=',
           47: '[',
           48: ']',
           49: '\\',
           52: '\'',
           54: ',',
           55: '.',
           62: 'f5',
           74: '^home',
           76: 'delete',
           77: '^end',
           79: 'right',
           80: 'left'
         }

ualtchars = {
           0: '',
           4: 'á',
           8: 'é',
           12: 'í',
           18: 'ó',
           24: 'ú',
           30: '¹',
           31: '²',
           32: '³',
           33: '⁴',
           34: '⁵',
           35: '⁶',
           36: '⁷',
           37: '⁸',
           38: '⁹',
           39: '⁰',
           40: 'enter',
           41: 'esc',
           42: 'backspace',
           43: 'tab',
           44: ' ',
           45: '-',
           46: '=',
           47: '[',
           48: ']',
           49: '\\',
           51: ';',
           52: '\'',
           54: ',',
           55: '.',
           56: '/',
           57: 'caps',
           62: 'f5',
           74: 'home',
           75: 'pgup',
           76: 'delete', 
           77: 'end',
           78: 'pgdn',
           79: 'right',
           80: 'left',
           81: 'down',
           82: 'up'
         }

ualtshiftchars = {
           0: '',
           4: 'Á',
           8: 'É',
           12: 'Í',
           18: 'Ó',
           24: 'Ú',
           30: '¹',
           31: '²',
           32: '³',
           33: '⁴',
           34: '⁵',
           35: '⁶',
           36: '⁷',
           37: '⁸',
           38: '⁹',
           39: '⁰',
           40: 'enter',
           41: 'esc',
           42: 'backspace',
           43: 'tab',
           44: ' ',
           45: '-',
           46: '=',
           47: '[',
           48: ']',
           49: '\\',
           51: ';',
           52: '\'',
           54: ',',
           55: '.',
           56: '/',
           57: 'caps',
           62: 'f5',
           74: 'home',
           75: 'pgup',
           76: 'delete', 
           77: 'end',
           78: 'pgdn',
           79: 'right',
           80: 'left',
           81: 'down',
           82: 'up'
         }

ushiftchars = {
           0: '',
           30: '!',
           31: '@',
           32: '#',
           33: '$',
           34: '%',
           35: '^',
           36: '&',
           37: '*',
           38: '(',
           39: ')',
           40: 'enter',
           42: 'backspace',
           43: '+tab',
           44: ' ',
           45: '_',
           46: '+',
           47: '{',
           48: '}',
           49: '|',
           50: '|',
           51: ':',
           52: '"',
           53: '~',
           54: '<',
           55: '>',
           56: '?',
           62: 'f5',
           74: 'home',
           76: 'delete',
           77: 'end',
           79: '+right',
           80: '+left'
         }

uctrlshiftchars = {
           0: '',
           30: '1',
           31: '2',
           32: '3',
           33: '4',
           34: '5',
           35: '6',
           36: '7',
           37: '8',
           38: '9',
           39: '0',
           40: 'enter',
           42: 'backspace',
           44: ' ',
           45: '^-',
           46: '^=',
           47: '[',
           48: ']',
           49: '\\',
           52: '\'',
           54: ',',
           55: '.',
           62: 'f5',
           74: '^home',
           76: 'delete',
           77: '^end',
           79: 'right',
           80: 'left'
         }

keys = {
         True:  {
                  True:  shiftalphachars,
                  False: shiftchars
                },
         False: {
                  True:  alphachars,
                  False: chars
                }
       }

ukeys = {
          True:  {
                   True:  {
                            True:  {},
                            False: {}
                          },
                   False: {
                            True:  uctrlshiftchars,
                            False: uctrlchars
                          }
                 },
          False: {
                   True:  {
                            True:  ualtshiftchars,
                            False: ualtchars
                          },
                   False: {
                            True:  ushiftchars,
                            False: uchars
                          }
                 }
        }

uchars[0] = ''
for c in range(4, 30):
  uchars[c] = chr(c + 93)
  uctrlchars[c] = '^' + chr(c + 93)
  ushiftchars[c] = chr(c + 61)
  uctrlshiftchars[c] = '^+' + chr(c + 93)

key = -1
alpha = False
shift = False
udata = [0, 0, 0, 0, 0, 0, 0, 0]
ulastkey = 0
ukey = 0
holdtime = 0
ctrl = False
alt = False
ushift = False

clearmodifiers = False

def init():
  eval('uopen()')
  try:
    while len(eval('usbrecv')):
      pass
  except:
    pass

def getkey():
  try:
    return keys[shift][alpha][key]
  except:
    return ''

def ugetkey():
  try:
    return ukeys[ctrl][alt][ushift][ukey]
  except:
    return ''

def uisdown(k):
  try:
    for l in udata[2:]:
      if ukeys[ctrl][alt][ushift][l] == k:
        return True
  except:
    pass
  return False

def testkey(k):
  return getkey() == k or ugetkey() == k

def update():
  global key
  global ukey
  global ulastkey
  global udata
  global holdtime
  global ctrl
  global alt
  global ushift
  global alpha
  global shift
  global clearmodifiers
  eval('uopen')
  if clearmodifiers:
    alpha = False
    shift = False
    clearmodifiers = False
  key = int(eval('getkey'))
  alpha = bool((keyboard() >> 36) & 1)
  shift = bool((keyboard() >> 41) & 1)
  d = eval('usbrecv')
  if d:
    udata = d
  elif d == 0:
    udata = [0, 0, 0, 0, 0, 0, 0, 0]
  ukey = 0
  try:
    keyindex = udata[2:].index(0)
  except ValueError:
    keyindex = 7
  keyindex = keyindex % 6 + 1
  if holdtime > 500 and udata[keyindex] != 0:
    ukey = udata[keyindex]
    eval('wait(0.001 * {})'.format(max(40 - time.dt, 1)))
  if udata[keyindex] != ulastkey:
    ukey = udata[keyindex]
    ulastkey = udata[keyindex]
    holdtime = 0
  else:
    holdtime += time.dt
  mod = int(udata[0])
  ctrl = bool((mod & 1) or (mod & 16))
  alt = bool((mod & 4) or (mod & 64))
  ushift = bool((mod & 2) or (mod & 32))